'use client'

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import { fetchLeaderboard, fetchMyRank } from "@/app/lib/api"

export default function Page() {
  const { contest_id } = useParams()
  const [data, setData] = useState<any[]>([])
  const [me, setMe] = useState<any>(null)

  useEffect(() => {
    fetchLeaderboard(contest_id as string).then(setData)
    fetchMyRank(contest_id as string).then(setMe)
  }, [contest_id])

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">
        Contest {contest_id} Leaderboard
      </h1>

      {me && (
        <div className="bg-yellow-100 p-3 rounded mb-4">
          Your Rank: #{me.rank} — {me.points} pts
        </div>
      )}

      <div className="space-y-2">
        {data.map((row) => (
          <div
            key={row.user_id}
            className="flex justify-between p-3 bg-gray-50 border rounded"
          >
            <span>#{row.rank}</span>
            <span>User {row.user_id}</span>
            <span>{row.points} pts</span>
          </div>
        ))}
      </div>
    </div>
  )
}
