import { Code2 } from "lucide-react"

export default function Header() {
  return (
    <div className="h-14 flex items-center px-6 bg-white border-b shadow-sm">
      <div className="flex items-center gap-2 text-xl font-bold text-black">
        <Code2 className="w-6 h-6" />
        Codeforces
      </div>
    </div>
  )
}