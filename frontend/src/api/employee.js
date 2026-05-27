import http from './http'

export function getEmployees(params) {
  return http.get('/employees', { params })
}

export function getEmployee(id) {
  return http.get(`/employees/${id}`)
}

export function createEmployee(data) {
  return http.post('/employees', data)
}

export function updateEmployee(id, data) {
  return http.put(`/employees/${id}`, data)
}

export function deleteEmployee(id) {
  return http.delete(`/employees/${id}`)
}

export function getAllEmployees() {
  return http.get('/employees/all')
}

export function createEmployeeAccount(employeeId, data) {
  return http.post(`/employees/${employeeId}/account`, data)
}

export function deleteEmployeeAccount(employeeId) {
  return http.delete(`/employees/${employeeId}/account`)
}
