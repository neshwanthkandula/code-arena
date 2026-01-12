'use client'

import { usePathname, useRouter } from "next/navigation"

const links = [
  { name: "Problems", path: "/problems" },
  { name: "Contests", path: "/contests" },
  { name: "Login", path: "/login" },
  { name: "Logout", path: "/logout" },
]

export default function Sidebar() {
  const pathname = usePathname()
  const router = useRouter()

  return (
    <aside className="w-64 bg-white border-r p-2">
      <nav className="space-y-1">
        {links.map(link => {
          const active = pathname.startsWith(link.path)

          return (
            <button
              key={link.path}
              onClick={() => router.push(link.path)}
              className={`w-full text-left px-4 py-2 rounded transition ${
                active
                  ? "bg-gray-600 text-white"
                  : "hover:bg-gray-100 text-black"
              }`}
            >
              {link.name}
            </button>
          )
        })}
      </nav>
    </aside>
  )
}
