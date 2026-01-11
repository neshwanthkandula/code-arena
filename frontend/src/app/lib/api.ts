export async function submitCode(payload: {
  problem_slug: string
  source_code: string
  language_id: number
}) {
  const res = await fetch("http://localhost:8000/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })

  return res.json()
}

export async function Signup(username: string ,email : string,  password : string){
  const res = await fetch("http://localhost:8000/auth/signup",{
    method: "POST",
    credentials : "include",
    headers : { "Content-Type": "application/json" },
    body : JSON.stringify({ username , email, password })
  })
}

export async function login(email : string, password : string){
  const res = await fetch("http://localhost:8000/auth/login", {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email , password })
  })
  return res.json()
}




