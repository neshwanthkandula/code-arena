"use client"
import { useParams } from "next/navigation"
import axios from "axios"
import { useEffect, useState } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import rehypeHighlight from "rehype-highlight"
import "highlight.js/styles/github.css"


interface ViewDataProps {
    slug : string,
    title : string,
    statement : string
}
async function fetch_viewData(slug : string): Promise<ViewDataProps> {
  const res = await axios.get(`http://127.0.0.1:8000/problem/${slug}`)
  console.log(res)
  return res.data;
}

export default function Product() {
  const params = useParams()
  const [viewData , setviewData] = useState<ViewDataProps>();
    const [loading, setLoading] = useState(false)
    
    useEffect(() => {
      const getProblems = async () => {
        try {
          setLoading(true)
          const data = await fetch_viewData(params.slug as string)
          setviewData(data)
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
    <div>
        <div className="markdown-body max-w-4xl mx-auto p-6 bg-white rounded-lg shadow">
  <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]}>
    {viewData?.statement || ""}
  </ReactMarkdown>
</div>

    </div>
  )
}
