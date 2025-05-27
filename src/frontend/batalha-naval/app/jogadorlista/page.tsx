"use client"

import React, { useEffect, useState } from 'react';

function ListaDeJogadores() {
  const [jogadores, setJogadores] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJogadores = async () => {
      try {
        const response = await fetch('https://web-production-cc859.up.railway.app/jogadores/lista_de_jogadores');
        console.log('Response status:', response.status); 
        console.log('Response headers:', response.headers); 
        if (!response.ok) {
          throw new Error('Erro ao buscar jogadores');
        }
        const data = await response.json();
        setJogadores(data);
      } catch (error) {
        console.error('Erro:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchJogadores();
  }, []);

  if (loading) {
    return <p>Carregando jogadores...</p>;
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Lista de Jogadores</h1>
      <ul className="space-y-2">
        {jogadores.map((jogador, index) => (
          <li key={index} className="p-4 rounded shadow">
            {/* @ts-ignore */}
            <p>Nome: {jogador.nome}</p>
            {/* @ts-ignore */}
            <p>Email: {jogador.email}</p>
            {/* @ts-ignore */}
            <p>Pontuação: {jogador.pontuacao}</p>
            {/* Exiba outros campos conforme disponíveis */}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ListaDeJogadores;