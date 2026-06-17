import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { BASE_PATH } from '@/config/runtime'
import { AppShell } from '@/components/layout/AppShell'
import S0Main from '@/pages/S0_Main'
import S1Diagnosis from '@/pages/S1_Diagnosis'
import S2Ranking from '@/pages/S2_Ranking'
import S3Settings from '@/pages/S3_Settings'
import S4Report from '@/pages/S4_Report'
import ReportList from '@/pages/S4_Report/list'

export default function App() {
  return (
    <BrowserRouter basename={BASE_PATH}>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<S0Main />} />
          <Route path="/diagnosis" element={<S1Diagnosis />} />
          <Route path="/ranking" element={<S2Ranking />} />
          <Route path="/settings" element={<S3Settings />} />
          <Route path="/reports" element={<ReportList />} />
          <Route path="/reports/:id" element={<S4Report />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
