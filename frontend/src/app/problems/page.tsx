'use client'

import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/navigation'

interface ProblemProps {
  title: string,
  slug: string,
  status :string
}

async function fetchProblems(): Promise<ProblemProps[]> {
  const res = await axios.get("http://127.0.0.1:8000/problems")
  console.log(res)
  return res.data;
}

const Page = () => {
  const [problems, setProblems] = useState<ProblemProps[]>([])
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  
  useEffect(() => {
    const getProblems = async () => {
      try {
        setLoading(true)
        const fetchedProblems = await fetchProblems()
        setProblems(fetchedProblems)
      } catch (error) {
        console.error("Error fetching problems:", error)
      } finally {
        setLoading(false)
      }
    }
    
    getProblems()
  }, [])
  
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }


  return (
    <div className="p-6">
      <div className="text-2xl font-bold mb-4">Problems</div>
      <div className="space-y-3" >
        {problems.map((problem, index) => (
          <div key={index} className="flex fborder p-4 rounded-lg bg-gray-50" onClick={()=>{
                router.push(`/problems/${problem.slug}`)
            }}>
            <div className="font-medium w-11 ">{index + 1}</div>
            <div className="font-medium">{problem.title}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Page