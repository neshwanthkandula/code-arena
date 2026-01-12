
'use client'

import { useState } from "react"
import { login } from "../lib/api"
import { useRouter } from "next/navigation"

export default function LoginPage() {
  const [email, setemail] = useState("")
  const [password, setPassword] = useState("")
  const router = useRouter()

  async function handleLogin() {
    await login(email, password)
    router.push("/problems")
  }

  return (
    <div className="p-6 max-w-sm mx-auto space-y-4">
      <h1 className="text-xl font-bold">Login</h1>
      <input className="border w-full p-2" placeholder="email" onChange={e => setemail(e.target.value)} />
      <input className="border w-full p-2" type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button className="bg-black text-white w-full p-2" onClick={handleLogin}>
        Login
      </button>
    </div>
  )
}