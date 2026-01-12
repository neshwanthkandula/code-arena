import axios from "axios"

export async function submitCode(payload: {
  problem_slug: string
  source_code: string
  language_id: number
}) {
  const res = await fetch("http://localhost:8000/submit", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })

  return res.json()
}

export async function contest_submitCode(payload: {
  problem_slug: string
  source_code: string
  language_id: number
}) {

  console.log(payload)
  const res = await fetch("http://localhost:8000/contest/submit", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })

  console.log("submit contest")
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

interface contestsProps{
  contest_id : string,
  start_Time : string,
  Duration : any
}



export async function  get_Contests() : Promise<contestsProps[]> {
  const res = await axios.get("http://127.0.0.1:8000/contest")
  console.log(res)
  return res.data;
}

export interface ProblemProps{
  slug : string,
  title : string
}

export async function get_contest_probelms( contest_id : string) : Promise<ProblemProps[]>{
  const res = await axios.get(`http://localhost:8000/contest/${contest_id}/problems`)
  return res.data
}


export async function fetchLeaderboard(contestId: string) {
  const res = await fetch(`http://localhost:8000/leaderboard/${contestId}`, {
    credentials: "include"
  })
  return res.json()
}

export async function fetchMyRank(contestId: string) {
  const res = await fetch(`http://localhost:8000/leaderboard/${contestId}/me`, {
    credentials: "include"
  })
  return res.json()
}
