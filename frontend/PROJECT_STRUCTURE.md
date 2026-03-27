# PLT Frontend - Complete Project Structure

## Files Created

### Configuration Files

1. **package.json** (43 lines)
   - Next.js 14, React 18, all specified dependencies
   - Dev scripts: dev, build, start, lint

2. **next.config.js** (6 lines)
   - Standalone output for production
   - React strict mode enabled
   - SWC minify enabled

3. **tailwind.config.js** (70 lines)
   - Dark mode: class-based
   - Custom colors: primary, secondary, accent, danger
   - Custom fonts: Inter
   - Custom animations: fade-in, slide-up, slide-down, pulse-subtle
   - Theme extensions with proper color scales

4. **postcss.config.js** (5 lines)
   - Tailwind CSS + Autoprefixer

5. **tsconfig.json** (30 lines)
   - Target: ES2020
   - Strict mode enabled
   - Path alias: @/* → ./src/*
   - Proper JSX handling for Next.js 14

### Application Files

#### Root Layout & Styles
- **src/app/layout.tsx** - Root layout with Inter font, metadata, Providers wrapper
- **src/app/globals.css** - Tailwind directives + CSS custom properties for theming (light/dark modes)
- **src/app/page.tsx** - Home page with landing content

### Library Files

#### API & HTTP
- **src/lib/api.ts** - Axios instance with:
  - Base URL: http://localhost:8000/api/v1
  - JWT token auto-injection interceptor
  - 401 error handling (logout on auth failure)

#### Utilities
- **src/lib/utils.ts** - cn() helper (clsx + tailwind-merge), date formatters

#### Hooks (State Management & Data Fetching)
- **src/lib/hooks/useAuth.ts** - Zustand auth store with:
  - user, token, isLoading, error state
  - login(), register(), logout(), checkAuth() methods
  - localStorage persistence

- **src/lib/hooks/useWebSocket.ts** - WebSocket connection hook with:
  - connect/disconnect management
  - Auto-reconnect with configurable interval
  - Message handling and sending
  - isConnected status

- **src/lib/hooks/useApi.ts** - React Query hooks:
  - useBiomarkers()
  - useBiomarkerHistory(biomarkerId)
  - useDigitalTwin(userId?)
  - useContracts()
  - useProtocols()
  - useAgentSessions()
  - useInventory()
  - useLongevityScore(userId?)
  - useAgents()

- **src/lib/hooks/index.ts** - Barrel export of all hooks

### Type Definitions
- **src/types/index.ts** - Complete TypeScript interfaces:
  - User, UserProfile
  - Biomarker, BiomarkerHistory
  - DigitalTwin, SystemScore (11 systems)
  - Agent, AgentSession, AgentDecision
  - Protocol, DailyContract, ContractItem
  - Supplement, InventoryItem
  - LongevityScore, ScoreBreakdown
  - ApiError

### UI Components (src/components/ui/)

All components use 'use client' directive, are fully typed, support dark mode, and use Tailwind CSS.

1. **button.tsx** - Button component
   - Variants: default, outline, ghost, destructive
   - Sizes: sm, md, lg
   - isLoading prop with spinner

2. **card.tsx** - Card components
   - Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter
   - Composition-based structure

3. **badge.tsx** - Badge component
   - Variants: default, success, warning, danger, info
   - Rounded pill shape

4. **progress.tsx** - Progress bar
   - Radix UI primitive-based
   - Colors: primary, secondary, success, warning, danger
   - Optional animation

5. **input.tsx** - Text input field
   - Focus ring and accessibility features
   - Dark mode support

6. **textarea.tsx** - Textarea element
   - Auto-expand disabled (resize: none)
   - Focus ring styling

7. **skeleton.tsx** - Loading skeleton
   - Animated pulse effect

8. **avatar.tsx** - Avatar component
   - Avatar, AvatarImage, AvatarFallback
   - Radix UI based

9. **tabs.tsx** - Tabbed interface
   - Tabs, TabsList, TabsTrigger, TabsContent
   - Radix UI based

10. **dialog.tsx** - Modal dialog
    - Dialog, DialogTrigger, DialogContent, DialogHeader, DialogFooter, DialogTitle, DialogDescription
    - Portal-based, close button with X icon
    - Fade-in overlay animation

11. **dropdown.tsx** - Dropdown menu
    - DropdownMenu, DropdownMenuTrigger, DropdownMenuContent
    - MenuItem, CheckboxItem, RadioItem, Label, Separator
    - Radix UI based with nested menu support

12. **tooltip.tsx** - Tooltip
    - Tooltip, TooltipTrigger, TooltipContent
    - TooltipProvider for context
    - Radix UI based

13. **alert.tsx** - Alert boxes
    - Alert, AlertTitle, AlertDescription
    - Variants: info, success, warning, error

14. **spinner.tsx** - Loading spinner
    - Sizes: sm, md, lg
    - Colors: primary, secondary, white
    - SVG-based with animate-spin

15. **index.ts** - Barrel export of all UI components

### Component Infrastructure
- **src/components/providers.tsx** - React Query + Tooltip Provider setup
  - QueryClient with 5min stale time, 10min cache time
  - Default retry: 1, refetchOnWindowFocus: false

### Configuration Files
- **.env.example** - Environment variable template
- **.gitignore** - Standard Node/Next.js ignores

### Documentation
- **README.md** - Complete project documentation
- **PROJECT_STRUCTURE.md** - This file

## Directory Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           (Root layout with providers)
│   │   ├── globals.css          (Tailwind + CSS variables)
│   │   └── page.tsx             (Home page)
│   ├── components/
│   │   ├── ui/
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── progress.tsx
│   │   │   ├── input.tsx
│   │   │   ├── textarea.tsx
│   │   │   ├── skeleton.tsx
│   │   │   ├── avatar.tsx
│   │   │   ├── tabs.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── dropdown.tsx
│   │   │   ├── tooltip.tsx
│   │   │   ├── alert.tsx
│   │   │   ├── spinner.tsx
│   │   │   └── index.ts
│   │   └── providers.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   ├── utils.ts
│   │   └── hooks/
│   │       ├── useAuth.ts
│   │       ├── useWebSocket.ts
│   │       ├── useApi.ts
│   │       └── index.ts
│   └── types/
│       └── index.ts
├── package.json
├── next.config.js
├── tailwind.config.js
├── postcss.config.js
├── tsconfig.json
├── .env.example
├── .gitignore
├── README.md
└── PROJECT_STRUCTURE.md
```

## Key Features

### TypeScript Strictness
- Strict mode enabled
- No unused locals/parameters
- Type-safe imports with @/* alias

### Styling
- Tailwind CSS with custom color palette
- CSS custom properties for theming
- Dark mode with class-based toggle
- Responsive design utilities

### State Management
- Zustand for authentication
- React Query for async data
- Context for providers

### API Integration
- Axios with automatic JWT injection
- 401 error handling with redirect
- Configurable base URL

### UI/UX
- Radix UI primitives for accessibility
- Lucide icons for graphics
- Framer Motion for animations (installed, ready to use)
- Recharts for data visualization (installed, ready to use)

## Ready for Development

All files are syntactically correct and ready for:
1. `npm install` to install dependencies
2. `npm run dev` to start development server
3. Component building and page creation
4. API integration with backend
