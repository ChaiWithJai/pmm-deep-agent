import { useState, useRef, useEffect, useCallback } from 'react'
import { Client } from '@langchain/langgraph-sdk'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Send,
  Loader2,
  Target,
  MessageSquare,
  LayoutTemplate,
  Users,
  Sparkles,
  Globe,
  ChevronDown,
  Wrench,
  CheckCircle2,
  AlertCircle,
  Trash2,
  ExternalLink,
} from 'lucide-react'
import './index.css'

// Configuration
const LANGGRAPH_API_URL = import.meta.env.VITE_LANGGRAPH_API_URL || 'http://localhost:2024'
const ASSISTANT_ID = 'pmm-evaluator'

// Types
interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  toolCalls?: ToolCall[]
  timestamp: Date
}

interface ToolCall {
  id: string
  name: string
  args: Record<string, unknown>
  status: 'pending' | 'running' | 'completed' | 'error'
  result?: string
}

interface QuickAction {
  icon: React.ReactNode
  label: string
  prompt: string
}

// Quick actions for common PMM tasks
const QUICK_ACTIONS: QuickAction[] = [
  {
    icon: <Globe className="w-4 h-4" />,
    label: 'Analyze Homepage',
    prompt: 'Run a complete PMM audit on the homepage at ',
  },
  {
    icon: <Target className="w-4 h-4" />,
    label: '5-Second Test',
    prompt: 'Run a 5-second test on the homepage at ',
  },
  {
    icon: <MessageSquare className="w-4 h-4" />,
    label: 'Messaging Analysis',
    prompt: 'Analyze the messaging hierarchy and clarity on ',
  },
  {
    icon: <Users className="w-4 h-4" />,
    label: 'Competitor Compare',
    prompt: 'Compare my homepage against these competitors: ',
  },
  {
    icon: <LayoutTemplate className="w-4 h-4" />,
    label: 'Create Positioning',
    prompt: 'Create a positioning canvas for: ',
  },
  {
    icon: <Sparkles className="w-4 h-4" />,
    label: 'Generate Rewrites',
    prompt: 'Generate improved headline and subheadline options for ',
  },
]

// Tool name to display name mapping
const TOOL_DISPLAY_NAMES: Record<string, string> = {
  run_five_second_test: '5-Second Test',
  analyze_positioning: 'Positioning Analysis',
  analyze_messaging: 'Messaging Analysis',
  analyze_homepage_structure: 'Structure Analysis',
  detect_anti_patterns: 'Anti-Pattern Detection',
  generate_rewrite: 'Content Rewrite',
  build_competitive_frame: 'Competitive Frame',
  analyze_icp: 'ICP Analysis',
  run_complete_pmm_audit: 'Complete PMM Audit',
  fetch_homepage: 'Fetch Homepage',
  fetch_competitor_homepage: 'Fetch Competitor',
  analyze_landing_page: 'Landing Page Analysis',
  scrape_social_proof: 'Social Proof Scan',
  create_positioning_canvas: 'Positioning Canvas',
  create_messaging_framework: 'Messaging Framework',
  create_homepage_wireframe: 'Homepage Wireframe',
  generate_differentiation_statements: 'Differentiation Statements',
}

function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [threadId, setThreadId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [expandedTools, setExpandedTools] = useState<Set<string>>(new Set())
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const clientRef = useRef<Client | null>(null)

  // Initialize client
  useEffect(() => {
    clientRef.current = new Client({ apiUrl: LANGGRAPH_API_URL })
  }, [])

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Auto-resize textarea
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto'
      inputRef.current.style.height = `${Math.min(inputRef.current.scrollHeight, 200)}px`
    }
  }, [input])

  const createThread = useCallback(async () => {
    if (!clientRef.current) return null
    try {
      const thread = await clientRef.current.threads.create()
      setThreadId(thread.thread_id)
      return thread.thread_id
    } catch (err) {
      console.error('Failed to create thread:', err)
      setError('Failed to connect to PMM Agent. Make sure the server is running.')
      return null
    }
  }, [])

  const sendMessage = useCallback(async (messageText: string) => {
    if (!messageText.trim() || isLoading) return

    setError(null)
    setIsLoading(true)

    // Add user message
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: messageText,
      timestamp: new Date(),
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')

    // Get or create thread
    let currentThreadId = threadId
    if (!currentThreadId) {
      currentThreadId = await createThread()
      if (!currentThreadId) {
        setIsLoading(false)
        return
      }
    }

    // Create assistant message placeholder
    const assistantMessageId = crypto.randomUUID()
    const assistantMessage: Message = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      toolCalls: [],
      timestamp: new Date(),
    }
    setMessages(prev => [...prev, assistantMessage])

    try {
      const stream = clientRef.current!.runs.stream(currentThreadId, ASSISTANT_ID, {
        input: { messages: [{ role: 'user', content: messageText }] },
        streamMode: 'messages',
      })

      let accumulatedContent = ''
      const toolCalls: Map<string, ToolCall> = new Map()

      for await (const event of stream) {
        if (event.event === 'messages/partial') {
          // The data is an array of message objects
          const streamMessages = event.data as Array<{
            content?: string | Array<{ type: string; text?: string; id?: string; name?: string; input?: Record<string, unknown> }>
            type?: string
          }>
          const lastMessage = streamMessages[streamMessages.length - 1]

          // Extract content and tool calls
          let content: string | undefined
          if (typeof lastMessage?.content === 'string') {
            content = lastMessage.content
          } else if (Array.isArray(lastMessage?.content)) {
            // Handle content blocks format
            const textBlocks = lastMessage.content.filter((b) => b.type === 'text')
            content = textBlocks.map((b) => b.text || '').join('')

            // Extract tool use blocks
            const toolUseBlocks = lastMessage.content.filter((b) => b.type === 'tool_use')
            for (const tool of toolUseBlocks) {
              if (tool.id && tool.name && !toolCalls.has(tool.id)) {
                toolCalls.set(tool.id, {
                  id: tool.id,
                  name: tool.name,
                  args: tool.input || {},
                  status: 'running',
                })
              }
            }
          }

          if (content && content.length > 0) {
            accumulatedContent = content
          }

          setMessages(prev => prev.map(msg =>
            msg.id === assistantMessageId
              ? { ...msg, content: accumulatedContent, toolCalls: Array.from(toolCalls.values()) }
              : msg
          ))
        }

        if (event.event === 'messages/complete') {
          // Mark all tool calls as completed
          for (const [id, tc] of toolCalls) {
            toolCalls.set(id, { ...tc, status: 'completed' })
          }

          setMessages(prev => prev.map(msg =>
            msg.id === assistantMessageId
              ? { ...msg, toolCalls: Array.from(toolCalls.values()) }
              : msg
          ))
        }
      }
    } catch (err) {
      console.error('Stream error:', err)
      setError('Failed to get response from PMM Agent. Please try again.')
      setMessages(prev => prev.filter(msg => msg.id !== assistantMessageId))
    } finally {
      setIsLoading(false)
    }
  }, [threadId, isLoading, createThread])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(input)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage(input)
    }
  }

  const handleQuickAction = (action: QuickAction) => {
    setInput(action.prompt)
    inputRef.current?.focus()
  }

  const toggleToolExpand = (toolId: string) => {
    setExpandedTools(prev => {
      const next = new Set(prev)
      if (next.has(toolId)) {
        next.delete(toolId)
      } else {
        next.add(toolId)
      }
      return next
    })
  }

  const clearConversation = () => {
    setMessages([])
    setThreadId(null)
    setError(null)
  }

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: '#FAF9F6' }}>
      {/* Header - CashIsClay x PIE Style */}
      <header className="border-b border-gray-200 bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex flex-col">
              <h1 className="font-serif text-xl font-semibold" style={{ color: '#1E3A5F' }}>
                CashIsClay
              </h1>
              <span className="text-xs tracking-wide" style={{ color: '#718096' }}>
                powered by <a href="https://princetonideaexchange.com" target="_blank" rel="noopener noreferrer" className="hover:underline" style={{ color: '#D2691E' }}>Princeton Idea Exchange</a>
              </span>
            </div>
          </div>
          <nav className="flex items-center gap-6">
            <a href="https://cashisclay.com" target="_blank" rel="noopener noreferrer" className="text-sm hover:underline" style={{ color: '#4A5568' }}>Course</a>
            <a href="https://chaiwithjai.com" target="_blank" rel="noopener noreferrer" className="text-sm hover:underline" style={{ color: '#4A5568' }}>Blog</a>
            {messages.length > 0 && (
              <button
                onClick={clearConversation}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                style={{ color: '#718096' }}
                title="Clear conversation"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            )}
          </nav>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-4 py-8">
          {messages.length === 0 ? (
            // Empty state - Enterprise Champion positioning
            <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-10"
              >
                <p className="text-sm tracking-widest mb-4" style={{ color: '#718096' }}>— See Why Your Team's Messaging Isn't Working —</p>
                <h2 className="font-serif text-4xl md:text-5xl font-bold mb-4" style={{ color: '#1E3A5F' }}>
                  The PMM Skills Gap<br />
                  <span className="text-2xl md:text-3xl font-normal" style={{ color: '#D2691E' }}>Is Costing You Conversions</span>
                </h2>
                <p className="text-lg max-w-lg mx-auto" style={{ color: '#4A5568' }}>
                  Run the same positioning audit Fortune 500 consultants use. Then train your team to fix it — or bring us in to do it with you.
                </p>
              </motion.div>

              {/* Quick Actions - PIE style cards */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 w-full max-w-2xl mb-8">
                {QUICK_ACTIONS.map((action, index) => (
                  <motion.button
                    key={action.label}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    onClick={() => handleQuickAction(action)}
                    className="group relative p-4 rounded-lg bg-white border border-gray-200 hover:border-[#D2691E] hover:shadow-md transition-all text-left"
                  >
                    <div className="w-8 h-8 rounded-lg flex items-center justify-center mb-3" style={{ backgroundColor: '#F5F3EE', color: '#D2691E' }}>
                      {action.icon}
                    </div>
                    <span className="text-sm font-medium" style={{ color: '#1E3A5F' }}>{action.label}</span>
                  </motion.button>
                ))}
              </div>

              {/* Triple CTA - Audit → Train → Hire */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="flex flex-col sm:flex-row gap-4 items-center"
              >
                <button
                  onClick={() => inputRef.current?.focus()}
                  className="inline-flex items-center gap-2 px-6 py-3 rounded-full text-white font-medium transition-transform hover:scale-105"
                  style={{ backgroundColor: '#D2691E' }}
                >
                  Audit Your Homepage
                </button>
                <a
                  href="https://cashisclay.com"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-6 py-3 rounded-full font-medium border-2 transition-all hover:bg-[#1E3A5F] hover:text-white"
                  style={{ borderColor: '#1E3A5F', color: '#1E3A5F' }}
                >
                  Train Your Team
                  <ExternalLink className="w-4 h-4" />
                </a>
                <a
                  href="https://calendly.com/chaiwithjai/30min"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-6 py-3 rounded-full font-medium border-2 transition-all hover:bg-[#1E3A5F] hover:text-white"
                  style={{ borderColor: '#1E3A5F', color: '#1E3A5F' }}
                >
                  Bring In An Expert
                </a>
              </motion.div>

              {/* Value prop */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="mt-8 p-4 rounded-xl max-w-xl"
                style={{ backgroundColor: '#F5F3EE' }}
              >
                <p className="text-sm" style={{ color: '#4A5568' }}>
                  <strong style={{ color: '#1E3A5F' }}>Why this exists:</strong> Most marketing teams can write copy but can't do positioning. This tool shows you exactly where the gaps are. Then you decide: <a href="https://cashisclay.com" target="_blank" rel="noopener noreferrer" className="underline hover:no-underline" style={{ color: '#D2691E' }}>train your team</a> ($2,197), or <a href="https://calendly.com/chaiwithjai/30min" target="_blank" rel="noopener noreferrer" className="underline hover:no-underline" style={{ color: '#D2691E' }}>bring in Princeton Idea Exchange</a> for hands-on facilitation.
                </p>
              </motion.div>

              <p className="mt-6 text-sm" style={{ color: '#718096' }}>
                Try: "Run a 5-second test on https://yourcompany.com"
              </p>
            </div>
          ) : (
            // Messages
            <div className="space-y-6">
              <AnimatePresence mode="popLayout">
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className={`max-w-[85%] ${message.role === 'user' ? 'order-2' : ''}`}>
                      {/* User message */}
                      {message.role === 'user' && (
                        <div className="rounded-2xl rounded-tr-md px-4 py-3 text-white" style={{ backgroundColor: '#D2691E' }}>
                          <p className="whitespace-pre-wrap">{message.content}</p>
                        </div>
                      )}

                      {/* Assistant message */}
                      {message.role === 'assistant' && (
                        <div className="space-y-3">
                          {/* Tool calls */}
                          {message.toolCalls && message.toolCalls.length > 0 && (
                            <div className="space-y-2">
                              {message.toolCalls.map((tc) => (
                                <div
                                  key={tc.id}
                                  className="bg-white border border-gray-200 rounded-xl overflow-hidden"
                                >
                                  <button
                                    onClick={() => toggleToolExpand(tc.id)}
                                    className="w-full flex items-center justify-between p-3 hover:bg-gray-50 transition-colors"
                                  >
                                    <div className="flex items-center gap-2">
                                      {tc.status === 'running' ? (
                                        <Loader2 className="w-4 h-4 animate-spin" style={{ color: '#D2691E' }} />
                                      ) : tc.status === 'completed' ? (
                                        <CheckCircle2 className="w-4 h-4" style={{ color: '#38A169' }} />
                                      ) : tc.status === 'error' ? (
                                        <AlertCircle className="w-4 h-4 text-red-500" />
                                      ) : (
                                        <Wrench className="w-4 h-4" style={{ color: '#718096' }} />
                                      )}
                                      <span className="text-sm font-medium" style={{ color: '#1E3A5F' }}>
                                        {TOOL_DISPLAY_NAMES[tc.name] || tc.name}
                                      </span>
                                    </div>
                                    <ChevronDown
                                      className={`w-4 h-4 transition-transform ${
                                        expandedTools.has(tc.id) ? 'rotate-180' : ''
                                      }`}
                                      style={{ color: '#718096' }}
                                    />
                                  </button>
                                  <AnimatePresence>
                                    {expandedTools.has(tc.id) && (
                                      <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: 'auto', opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        className="border-t border-gray-200"
                                      >
                                        <pre className="p-3 text-xs overflow-x-auto" style={{ color: '#4A5568', backgroundColor: '#F5F3EE' }}>
                                          {JSON.stringify(tc.args, null, 2)}
                                        </pre>
                                      </motion.div>
                                    )}
                                  </AnimatePresence>
                                </div>
                              ))}
                            </div>
                          )}

                          {/* Content */}
                          {message.content && typeof message.content === 'string' && message.content.trim() && (
                            <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-md px-4 py-3">
                              <div className="prose">
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                  {message.content}
                                </ReactMarkdown>
                              </div>
                            </div>
                          )}

                          {/* Loading state */}
                          {!message.content && (!message.toolCalls || message.toolCalls.length === 0) && (
                            <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-md px-4 py-3">
                              <div className="flex items-center gap-1">
                                <div className="w-2 h-2 rounded-full typing-dot" style={{ backgroundColor: '#D2691E' }} />
                                <div className="w-2 h-2 rounded-full typing-dot" style={{ backgroundColor: '#D2691E' }} />
                                <div className="w-2 h-2 rounded-full typing-dot" style={{ backgroundColor: '#D2691E' }} />
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </main>

      {/* Error banner */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="fixed bottom-24 left-1/2 -translate-x-1/2 bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-lg flex items-center gap-2 shadow-lg"
          >
            <AlertCircle className="w-4 h-4" />
            <span className="text-sm">{error}</span>
            <button
              onClick={() => setError(null)}
              className="ml-2 text-red-400 hover:text-red-600"
            >
              ×
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Input area */}
      <footer className="border-t border-gray-200 bg-white/80 backdrop-blur-sm sticky bottom-0">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <form onSubmit={handleSubmit} className="relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about positioning, messaging, or paste a URL to analyze..."
              rows={1}
              className="w-full bg-white border border-gray-200 rounded-xl px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-[#D2691E] focus:border-transparent resize-none"
              style={{ color: '#1E3A5F' }}
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="absolute right-2 bottom-2 p-2 rounded-lg text-white disabled:opacity-50 disabled:cursor-not-allowed hover:opacity-90 transition-opacity"
              style={{ backgroundColor: '#D2691E' }}
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </form>
          <p className="text-center text-xs mt-2" style={{ color: '#718096' }}>
            Built by <a href="https://chaiwithjai.com" target="_blank" rel="noopener noreferrer" className="hover:underline" style={{ color: '#D2691E' }}>Jai Bhagat</a> • April Dunford & Fletch PMM frameworks • <a href="https://github.com/ChaiWithJai/pmm-deep-agent" target="_blank" rel="noopener noreferrer" className="hover:underline" style={{ color: '#D2691E' }}>View Source</a>
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
