"use client"

import { useState } from "react"
import { contest_submitCode, submitCode } from "../../src/app/lib/api"

interface SubmitButtonProps {
  problemSlug: string
  sourceCode: string
  languageId: number
  onResult: (result: any) => void
}

export default function ProblemSubmitButton({
  problemSlug,
  sourceCode,
  languageId,
  onResult
}: SubmitButtonProps) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleClick() {
    if (!sourceCode.trim()) {
      setError("Code cannot be empty")
      return
    }

    try {
      setLoading(true)
      setError(null)

      const result = await submitCode({
        problem_slug: problemSlug,
        source_code: sourceCode,
        language_id: languageId
      })

      onResult(result)
    } catch {
      setError("Submission failed. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-end gap-2">
      <button
        onClick={handleClick}
        disabled={loading}
        className={`
          min-w-[120px]
          px-4 py-2
          rounded-md
          text-sm font-semibold
          transition-all
          focus:outline-none focus:ring-2 focus:ring-blue-500
          ${
            loading
              ? "bg-gray-400 cursor-not-allowed text-white"
              : "bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white"
          }
        `}
      >
        {loading ? "Running..." : "Submit"}
      </button>

      {error && (
        <span className="text-xs text-red-500">
          {error}
        </span>
      )}
    </div>
  )
}
