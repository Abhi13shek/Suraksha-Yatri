import { useState } from "react";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!username || !password) {
      setError("Please fill all fields");
      return;
    }

    // Simulated login
    if (username === "abhishek" && password === "1234") {
      localStorage.setItem("loggedInUser", username);
      window.location.href = "/tourism";
    } else {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-[#0f2027]/90 via-[#203a43]/90 to-[#2c5364]/90 text-white relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 opacity-20 bg-[url('https://upload.wikimedia.org/wikipedia/commons/8/80/World_map_-_low_resolution.svg')] bg-cover bg-center"></div>

      {/* Heading */}
      <h1 className="text-4xl font-bold text-yellow-300 mb-2 z-10">
        Suraksha Yatri
      </h1>
      <p className="text-gray-300 mb-6 z-10">Login to continue</p>

      {/* Login Box */}
      <div className="z-10 w-[360px] bg-white/10 backdrop-blur-xl p-10 rounded-2xl shadow-xl">
        <h2 className="text-xl mb-5">Secure Login</h2>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <input
              type="text"
              placeholder="Enter Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full p-3 rounded-lg bg-white/20 placeholder-gray-300 outline-none"
            />
          </div>

          <div className="mb-4">
            <input
              type="password"
              placeholder="Enter Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full p-3 rounded-lg bg-white/20 placeholder-gray-300 outline-none"
            />
          </div>

          {error && (
            <p className="text-red-400 text-sm mb-3">{error}</p>
          )}

          <button
            type="submit"
            className="w-full py-3 rounded-xl bg-gradient-to-r from-[#ff512f] to-[#dd2476] font-semibold hover:scale-105 transition-transform"
          >
            Login
          </button>
        </form>
      </div>

      {/* Footer */}
      <footer className="absolute bottom-3 text-black text-sm">
        © 2025 Suraksha Yatri Project | All Rights Reserved
      </footer>
    </div>
  );
}

