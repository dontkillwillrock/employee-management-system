import http from './http'

export function getAttendances(params) {
  return http.get('/attendances', { params })
}

export function checkIn(employeeId) {
  return http.post('/attendances/checkin', { employee_id: employeeId })
}

export function checkOut(employeeId) {
  return http.post('/attendances/checkout', { employee_id: employeeId })
}

export function applyLeave(data) {
  return http.post('/attendances/leave', data)
}

export function getLeaves(params) {
  return http.get('/attendances/leave', { params })
}

export function approveLeave(id, action) {
  return http.put(`/attendances/leave/${id}/approve`, { action })
}
