import { NavLink, Outlet } from 'react-router-dom'
import { AnalysisStatusCard } from '@/components/analysis/AnalysisStatusCard'

const NAV_ITEMS = [
  { to: '/',          label: '대시보드',    icon: '🗺' },
  { to: '/diagnosis', label: '국가 진단',   icon: '🔍' },
  { to: '/ranking',   label: '권역 순위',   icon: '📊' },
  { to: '/settings',  label: '설정',        icon: '⚙️' },
  { to: '/reports',   label: '보고서',      icon: '📄' },
]

export function AppShell() {
  return (
    <div className="flex min-h-screen w-full">
      {/* 사이드 네비게이션 */}
      <nav className="w-60 shrink-0 bg-ink text-[#cdd6d1] flex flex-col sticky top-0 h-screen overflow-y-auto">
        <div className="px-6 py-6 border-b border-[#2a3531]">
          <h1 className="text-[15px] font-bold text-white leading-tight">
            오토금융<br />해외진출 진단
          </h1>
          <p className="text-[11px] text-[#7c8a84] mt-1.5 tracking-widest uppercase">
            Console v0.2
          </p>
        </div>

        <div className="flex-1 py-4">
          <p className="px-6 pt-2 pb-1 text-[10px] tracking-widest uppercase text-[#6b7771]">메뉴</p>
          {NAV_ITEMS.map(item => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-6 py-2.5 text-[13.5px] border-l-[2.5px] transition-all ${
                  isActive
                    ? 'text-white border-accent bg-[#1a2e27]'
                    : 'text-[#b6c0bb] border-transparent hover:text-white hover:bg-[#1a2e27]/50'
                }`
              }
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </div>
      </nav>

      {/* 메인 콘텐츠 */}
      <main className="flex-1 min-w-0 overflow-auto">
        <Outlet />
      </main>

      {/* 전 화면 공통 분석 상태 카드 */}
      <AnalysisStatusCard />
    </div>
  )
}
