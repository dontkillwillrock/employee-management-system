import http from './http'

export function getSalaries(params) {
  return http.get('/salaries', { params })
}

export function createSalary(data) {
  return http.post('/salaries', data)
}

export function updateSalary(id, data) {
  return http.put(`/salaries/${id}`, data)
}

export function deleteSalary(id) {
  return http.delete(`/salaries/${id}`)
}

export function paySalary(id) {
  return http.put(`/salaries/${id}/pay`)
}
