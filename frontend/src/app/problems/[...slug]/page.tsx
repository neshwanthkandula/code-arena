"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import axios from "axios"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import rehypeHighlight from "rehype-highlight"
import Editor from "@monaco-editor/react"
import SubmitButton from "../../../../components/ui/submitbutton"
import "highlight.js/styles/github.css"

interface Problem {
  slug: string
  title: string
  statement: string
  difficulty?: string
  tags?: string[]
}

export default function ProblemPage() {
  const params = useParams()
  const slug = Array.isArray(params.slug) ? params.slug[0] : params.slug

  const [problem, setProblem] = useState<Problem | null>(null)
  const [code, setCode] = useState("")
  const [languageId, setLanguageId] = useState(71)
  const [result, setResult] = useState<any>(null)

  useEffect(() => {
    async function load() {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/problem/${slug}`)
        setProblem(res.data)
      } catch (err) {
        console.error("Failed to load problem", err)
      }
    }
    load()
  }, [slug])

  if (!problem) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  const verdict = result?.status?.description
  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center px-6 py-4 border-b">
        <h1 className="text-xl font-bold">{problem.title}</h1>
      </div>

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left: Problem */}
        <div className="w-1/2 p-6 overflow-y-auto border-r">
          <article className="prose max-w-none">
           <ReactMarkdown>{problem.statement}</ReactMarkdown>
          </article>
        </div>

        {/* Right: Editor */}
        <div className="w-1/2 flex flex-col">
          <div className="p-2 border-b flex justify-between">
            <select
              value={languageId}
              onChange={(e) => setLanguageId(Number(e.target.value))}
              className="border px-2 py-1"
            >
              <option value={71}>Python</option>
              <option value={54}>C++</option>
            </select>


            <SubmitButton
              problemSlug={slug as string}
              sourceCode={code}
              languageId={languageId}
              onResult={setResult}
            />
          </div>

          <Editor
            height="100%"
            defaultLanguage="python"
            value={code}
            onChange={(v) => setCode(v || "")}
            theme="vs-dark"
          />
        </div>
      </div>

      {/* Result */}
      {verdict && (
        <div className="p-3 border-t flex justify-center items-center bg-gray-100">
          <span
            className={`text-lg font-bold ${
              verdict === "Accepted" ? "text-green-600" : "text-red-600"
            }`}
          >
            {verdict === "Accepted" ? "✓ Accepted" : "✗ Wrong Answer"}
          </span>
        </div>
      )}
    </div>
  )
}
