'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [tabuleiros, setTabuleiros] = useState<string[][] | null>(null);
  const [loading, setLoading] = useState(true);
  const [nomeJogador, setNomeJogador] = useState<string | undefined>(undefined);
  const [inputs, setInputs] = useState({
    embarcacao: '',
    coordX: '',
    coordY: '',
    orientacao: '',
  });
  const [embarcacoesRestantes, setEmbarcacoesRestantes] = useState({
    Submarino: 2,
    NavioPequeno: 1,
    NavioMédio: 1,
    PortaAviões: 1,
  });
  
  const [message, setMessage] = useState<string>('');

  const router = useRouter();
  const [isClient, setIsClient] = useState(false);

  const token = '123';
  const id = 1;

  const cor = {
    '1': '#90EE90',
    '2': '#006400',
    '3': '#3CB371',
    '4': '#2E8B57',
    'default': '#00BFFF',
  };

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    if (isClient) {
      const storedNomeJogador = localStorage.getItem('nomeJogador');
      if (storedNomeJogador) {
        setNomeJogador(storedNomeJogador);
      } else {
        router.push(`/`); // Se o nome do jogador não for encontrado, redireciona para a página inicial
      }
    }
  }, [isClient, router]);

  useEffect(() => {
    if (!nomeJogador) return;

    const fetchTabuleiros = async () => {
      try {
        const url = `https://web-production-cc859.up.railway.app/partida/tabuleiro/${id}/${nomeJogador}`;
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Erro ao buscar os tabuleiros');
        }
        const data: string[][] = await response.json();

        const tabuleirosProcessados = data.map(tabuleiro =>
          tabuleiro.map(linha => linha.split(''))
        );
        
        {/* @ts-ignore */}
        setTabuleiros(tabuleirosProcessados);

        // Verifica se todas as embarcações foram posicionadas
        const todasPosicionadas = Object.values(embarcacoesRestantes).every(quantidade => quantidade === 0);
        
        // Se todas as embarcações foram posicionadas, redireciona o jogador
        if (todasPosicionadas) {
          const dataResponse = await response.json();
          if (dataResponse.message === "Embarcações posicionadas" || todasPosicionadas) {
            localStorage.setItem('nomeJogador', nomeJogador);
            router.push('/partida'); // Redireciona para a tela de partida
          }
        }
      } catch (error) {
        console.error('Erro:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTabuleiros();
  }, [id, nomeJogador, embarcacoesRestantes, router]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setInputs(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async () => {
    const { embarcacao, coordX, coordY, orientacao } = inputs;

    if (embarcacoesRestantes[embarcacao as keyof typeof embarcacoesRestantes] <= 0) {
      alert(`Todas as embarcações do tipo ${embarcacao} já foram colocadas.`);
      return;
    }

    try {
      const url = `https://web-production-cc859.up.railway.app/partida/tabuleiro/peças/${id}/${nomeJogador}/${embarcacao}/${coordX}/${coordY}/${orientacao}`;
      const response = await fetch(url, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();
      setMessage(data.message)

      if (!response.ok) {
        throw new Error('Erro ao enviar os dados para a API');
      }
      const updatedResponse = await fetch(
        `https://web-production-cc859.up.railway.app/partida/tabuleiro/${id}/${nomeJogador}`
      );
      const updatedData: string[][] = await updatedResponse.json();
      const tabuleirosProcessados = updatedData.map(tabuleiro =>
        tabuleiro.map(linha => linha.split(''))
      );
      {/* @ts-ignore */}
      setTabuleiros(tabuleirosProcessados);

      // Atualiza a quantidade de embarcações restantes
      setEmbarcacoesRestantes(prev => ({
        ...prev,
        [embarcacao]: Math.max(prev[embarcacao as keyof typeof prev] - 1, 0),
      }));

    } catch (error) {
      console.error('Erro:', error);
    }
  };

  const mostrarEmbarcacoesRestantes = () => {
    const mensagem = Object.entries(embarcacoesRestantes)
      .map(([tipo, quantidade]) => `${tipo}: ${quantidade} restantes`)
      .join('\n');
    alert(`Embarcações restantes:\n${mensagem}`);
  };

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (!tabuleiros || tabuleiros.length < 2) {
    return <div>Erro ao carregar os tabuleiros.</div>;
  }

  const renderizarTabuleiro = (tabuleiro: string[][]) => {
    const letras = ['A', 'B', 'C', 'D', 'E'];

    return (
      <div style={{ display: 'inline-block' }}>
        <div style={{ display: 'flex', marginBottom: '5px' }}>
          <div style={{ width: '35px' }}></div>
          {['1', '2', '3', '4', '5'].map((numero, i) => (
            <div
              key={i}
              style={{
                width: '53px',
                height: '30px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 'bold',
                
              }}
            >
              {numero}
            </div>
          ))}
        </div>

        {tabuleiro.map((linha, i) => (
          <div key={i} style={{ display: 'flex' }}>
            <div
              style={{
                width: '30px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 'bold',
                
              }}
            >
              {letras[i]}
            </div>
            {linha.map((celula, j) => (
              <div
                key={`${i}-${j}`}
                style={{
                  width: '50px',
                  height: '50px',
                  border: '1px solid black',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  backgroundColor: cor[celula as keyof typeof cor] || cor.default,
                  color: cor[celula as keyof typeof cor] ? cor[celula as keyof typeof cor] : cor.default,
                  margin: '1px',
                }}
              >
                {celula}
              </div>
            ))}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-around', width: '100%' }}>
        <div>
          <h2>Meu Tabuleiro</h2>
          {/* @ts-ignore */}
          {renderizarTabuleiro(tabuleiros[0])}
        </div>
      </div>

      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <h2>Coloque as embarcações</h2>
        {['embarcacao', 'coordX', 'coordY', 'orientacao'].map(field => (
          <div key={field} style={{ marginBottom: '10px' }}>
            <input
              type="text"
              name={field}
              placeholder={`Digite ${field}`}
              value={inputs[field as keyof typeof inputs]}
              onChange={handleInputChange}
              style={{ padding: '5px', width: '200px' }}
            />
          </div>
        ))}
        {message && (<p style={{
          color: message === 'Peça colocada' ? '#00FF00' : '#FF0000',
          fontWeight: 'bold',
        }}>
          {message}
        </p>)}
        <button onClick={handleSubmit} style={{ padding: '10px 20px', marginTop: '10px' }}>
          Enviar
        </button>
        <button
          onClick={mostrarEmbarcacoesRestantes}
          style={{ padding: '10px 20px', marginTop: '10px', marginLeft: '10px' }}
        >
          Mostrar Embarcações Restantes
        </button>
      </div>
    </div>
  );
}

