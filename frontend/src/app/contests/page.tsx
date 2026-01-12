'use client'

import React, { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { get_Contests } from '../lib/api'
import { BarChart2 } from 'lucide-react'

interface ContestProps {
  contest_id: string
  start_Time: string
  Duration: number
}

export default function Page() {
  const [contests, setContests] = useState<ContestProps[]>([])
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const fetchContests = async () => {
      try {
        setLoading(true)
        const data = await get_Contests()
        setContests(data)
      } catch (error) {
        console.error('Error fetching contests:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchContests()
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
      <div className="text-2xl font-bold mb-4">Contests</div>

      <div className="space-y-3">
        {contests.map((contest, index) => (
          <div
            key={contest.contest_id}
            className="flex items-center justify-between border p-4 rounded-lg bg-gray-50 hover:bg-gray-100"
          >
            {/* Left side: contest info (clickable) */}
            <div
              className="flex cursor-pointer flex-1"
              onClick={() => router.push(`/contests/${contest.contest_id}`)}
            >
              <div className="font-medium w-12">{index + 1}</div>

              <div className="flex flex-col">
                <div className="font-medium">{contest.contest_id}</div>
                <div className="flex gap-4 text-sm text-gray-600">
                  <div>
                    Starts: {new Date(contest.start_Time).toLocaleString()}
                  </div>
                  <div>
                    Duration: {contest.Duration} sec
                  </div>
                </div>
              </div>
            </div>

            {/* Right side: leaderboard icon */}
            <button
              onClick={(e) => {
                e.stopPropagation()
                router.push(`/standings/${contest.contest_id}`)
              }}
              className="p-2 rounded hover:bg-gray-200"
              title="View Standings"
            >
              <BarChart2 className="w-5 h-5 text-gray-600" />
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
