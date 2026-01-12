'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { get_contest_probelms } from '@/app/lib/api'

export interface ProblemProps {
  slug: string
  title: string
}

export default function Page() {
  const params = useParams()
  const router = useRouter()
  const contest_id = params.contest_id as string

  const [problems, setProblems] = useState<ProblemProps[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        setLoading(true)
        const res = await get_contest_probelms(contest_id)
        setProblems(res)
      } catch (err) {
        console.error('Error fetching contest problems:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchProblems()
  }, [contest_id])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="text-2xl font-bold mb-4">
        {contest_id} - Problems
      </div>

      <div className="space-y-3">
        {problems.map((problem, index) => (
          <div
            key={problem.slug}
            className="flex border p-4 rounded-lg bg-gray-50 cursor-pointer hover:bg-gray-100"
            onClick={() =>
              router.push(`/contests/${contest_id}/${problem.slug}`)
            }
          >
            <div className="font-medium w-12">{index + 1}</div>
            <div className="font-medium">{problem.title}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
