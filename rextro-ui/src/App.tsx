import { useState } from 'react'
import { Send, Bot, User } from 'lucide-react'
import type { FormEvent } from 'react'

interface Message {
  type: 'user' | 'bot'
  content: string
}

function App() {
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const parseMarkdown = (text: string): string => {
    if (!text) return ''
    
    // Headers
    text = text.replace(/^### (.*$)/gim, '<h3 class="text-lg font-bold mt-4 mb-2 text-gray-800">$1</h3>')
    text = text.replace(/^## (.*$)/gim, '<h2 class="text-xl font-bold mt-5 mb-3 text-gray-800">$1</h2>')
    text = text.replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold mt-6 mb-3 text-gray-900">$1</h1>')
    
    // Bold
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-blue-600">$1</strong>')
    
    // Italic
    text = text.replace(/\*(.*?)\*/g, '<em class="italic">$1</em>')
    
    // Code blocks
    text = text.replace(/```([\s\S]*?)```/g, '<pre class="bg-gray-800 text-gray-100 p-3 rounded-lg overflow-x-auto my-3 text-sm"><code>$1</code></pre>')
    
    // Inline code
    text = text.replace(/`([^`]+)`/g, '<code class="bg-gray-200 px-2 py-1 rounded text-sm font-mono text-red-600">$1</code>')
    
    // Links
    text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-blue-500 hover:text-blue-700 underline" target="_blank" rel="noopener noreferrer">$1</a>')
    
    // Unordered lists
    text = text.replace(/^\* (.*$)/gim, '<li class="ml-4 mb-1">• $1</li>')
    text = text.replace(/(<li.*<\/li>)/s, '<ul class="my-2 space-y-1">$1</ul>')
    
    // Ordered lists
    text = text.replace(/^\d+\. (.*$)/gim, '<li class="ml-4 mb-1">$1</li>')
    
    // Line breaks
    text = text.replace(/\n\n/g, '</p><p class="mb-3">')
    text = text.replace(/\n/g, '<br />')
    
    return `<p class="mb-3">${text}</p>`
  }

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!query.trim()) return

    const userMessage: Message = { type: 'user', content: query }
    setMessages(prev => [...prev, userMessage])
    setQuery('')
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:7000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          variables: {}
        }),
      })

      const data = await response.json()
      const botMessage: Message = { type: 'bot', content: data.answer }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: Message = { type: 'bot', content: 'Sorry, there was an error processing your request.' }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="max-w-4xl mx-auto px-4 py-6 sm:py-8">
        {/* Header */}
        <div className="text-center mb-6 sm:mb-8">
          <div className="flex items-center justify-center gap-3 mb-2">
            <Bot className="w-8 h-8 sm:w-10 sm:h-10 text-blue-600" />
            <h1 className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Rextro Chatbot
            </h1>
          </div>
          <p className="text-gray-600 text-sm sm:text-base">Ask me anything about Rextro</p>
        </div>

        {/* Chat Messages */}
        <div className="bg-white rounded-2xl shadow-xl mb-4 sm:mb-6 overflow-hidden">
          <div className="h-[50vh] sm:h-[60vh] overflow-y-auto p-4 sm:p-6 space-y-4">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full text-gray-400">
                <div className="text-center">
                  <Bot className="w-12 h-12 sm:w-16 sm:h-16 mx-auto mb-4 opacity-50" />
                  <p className="text-sm sm:text-base">Start a conversation by asking a question</p>
                </div>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex gap-3 ${msg.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
                >
                  <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    msg.type === 'user' ? 'bg-blue-600' : 'bg-purple-600'
                  }`}>
                    {msg.type === 'user' ? (
                      <User className="w-5 h-5 text-white" />
                    ) : (
                      <Bot className="w-5 h-5 text-white" />
                    )}
                  </div>
                  <div
                    className={`flex-1 max-w-[85%] sm:max-w-[75%] rounded-2xl px-4 py-3 ${
                      msg.type === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {msg.type === 'user' ? (
                      <p className="text-sm sm:text-base leading-relaxed">{msg.content}</p>
                    ) : (
                      <div
                        className="prose prose-sm sm:prose max-w-none leading-relaxed text-sm sm:text-base"
                        dangerouslySetInnerHTML={{ __html: parseMarkdown(msg.content) }}
                      />
                    )}
                  </div>
                </div>
              ))
            )}
            
            {isLoading && (
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div className="bg-gray-100 rounded-2xl px-4 py-3">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-xl p-3 sm:p-4">
          <div className="flex gap-2 sm:gap-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Type your question..."
              className="flex-1 px-4 py-2 sm:py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm sm:text-base transition-all"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="px-4 sm:px-6 py-2 sm:py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 font-medium text-sm sm:text-base"
            >
              <Send className="w-4 h-4 sm:w-5 sm:h-5" />
              <span className="hidden sm:inline">Send</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default App