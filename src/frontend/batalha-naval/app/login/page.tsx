"use client"

import { useState } from "react";

export default function Login() {
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      // Montar a URL dinâmica
      const url = `http://localhost:8000/autenticacao/${name}/${password}/`;

      // Fazer a requisição para o backend
      const response = await fetch(url, {
        method: "POST", // O método precisa ser POST, conforme o backend
      });

      if (response.ok) {
        const data = await response.json(); // Presume-se que o backend retorna dados úteis
        setMessage(`Bem-vindo, ${data.name || name}! Sessão registrada com sucesso.`);
        setName("");
        setPassword("");
      } else {
        const errorData = await response.json();
        setMessage(errorData.detail || "Nome ou senha incorretos.");
      }
    } catch (error) {
      console.error("Erro ao autenticar:", error);
      setMessage("Erro ao conectar com o servidor.");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Login</h1>
      <form
        onSubmit={handleLogin}
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "15px",
          maxWidth: "400px",
        }}
      >
        <label>
          Nome:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "8px",
              marginTop: "5px",
              border: "1px solid #ccc",
              borderRadius: "4px",
            }}
          />
        </label>
        <label>
          Senha:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{
              width: "100%",
              padding: "8px",
              marginTop: "5px",
              border: "1px solid #ccc",
              borderRadius: "4px",
            }}
          />
        </label>
        <button
          type="submit"
          style={{
            padding: "10px",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Entrar
        </button>
      </form>
      {message && (
        <p
          style={{
            marginTop: "20px",
            color: message.includes("Bem-vindo") ? "green" : "red",
          }}
        >
          {message}
        </p>
      )}
    </div>
  );
}