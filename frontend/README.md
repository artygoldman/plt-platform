# PLT Frontend

Personal Longevity Team health platform frontend built with Next.js 14, React 18, and TypeScript.

## Technology Stack

- **Framework**: Next.js 14
- **UI Library**: React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI primitives
- **State Management**: Zustand
- **Data Fetching**: Axios + React Query
- **Icons**: Lucide React
- **Charts**: Recharts
- **Animations**: Framer Motion

## Project Structure

```
src/
├── app/                 # Next.js app directory
│   ├── layout.tsx      # Root layout with providers
│   ├── globals.css     # Global styles and theme variables
│   └── page.tsx        # Home page
├── components/
│   ├── ui/             # Reusable UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── badge.tsx
│   │   ├── progress.tsx
│   │   ├── input.tsx
│   │   ├── textarea.tsx
│   │   ├── skeleton.tsx
│   │   ├── avatar.tsx
│   │   ├── tabs.tsx
│   │   ├── dialog.tsx
│   │   ├── dropdown.tsx
│   │   ├── tooltip.tsx
│   │   ├── alert.tsx
│   │   ├── spinner.tsx
│   │   └── index.ts    # Barrel export
│   └── providers.tsx    # React Query + Tooltip Provider setup
├── lib/
│   ├── api.ts          # Axios instance with JWT interceptors
│   ├── utils.ts        # cn() helper and formatting utilities
│   └── hooks/
│       ├── useAuth.ts      # Authentication state management (Zustand)
│       ├── useWebSocket.ts # WebSocket connection hook
│       ├── useApi.ts       # React Query data fetching hooks
│       └── index.ts        # Barrel export
└── types/
    └── index.ts        # All TypeScript interfaces

```

## Getting Started

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
npm run build
npm start
```

## Environment Variables

Create a `.env.local` file based on `.env.example`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

## Theming

The app uses CSS variables for theming with support for light and dark modes:

- **Colors**: Primary (emerald), Secondary (blue), Accent (amber), Danger (red)
- **Mode**: Class-based dark mode via Tailwind CSS
- **Font**: Inter (Google Fonts)

Theme variables are defined in `globals.css` and can be customized.

## Component Usage

### Button

```tsx
import { Button } from '@/components/ui';

<Button variant="default" size="lg">
  Click me
</Button>
```

### Card

```tsx
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui';

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>Content</CardContent>
</Card>
```

### Using Hooks

```tsx
import { useBiomarkers, useAuth } from '@/lib/hooks';

function Component() {
  const { data: biomarkers } = useBiomarkers();
  const { user, logout } = useAuth();

  return <div>...</div>;
}
```

## API Integration

The app uses Axios with automatic JWT token injection:

```tsx
import axiosInstance from '@/lib/api';

// Token is automatically added to Authorization header
const response = await axiosInstance.get('/biomarkers');
```

On 401 errors, the token is cleared and user is redirected to login.

## State Management

### Authentication (Zustand)

```tsx
import { useAuth } from '@/lib/hooks';

const { user, token, login, logout } = useAuth();
```

### Data Fetching (React Query)

```tsx
import { useBiomarkers } from '@/lib/hooks';

const { data, isLoading, error } = useBiomarkers();
```

## TypeScript

All components and utilities are fully typed. Type definitions are in `src/types/index.ts`.

## Tailwind CSS

Custom theme configuration in `tailwind.config.js`:

- Dark mode: class-based
- Colors: Custom color palette
- Fonts: Inter (system font fallbacks)
- Animations: Custom keyframes (fade-in, slide-up, etc.)

## Performance

- Standalone output for optimized builds
- React Query caching: 5 min stale, 10 min garbage collection
- Image optimization with Next.js
- Code splitting with dynamic imports
- CSS minification via Tailwind

## License

Proprietary - Personal Longevity Team
