<template>
  <div>
    <!-- 操作栏 -->
    <el-card shadow="hover" style="margin-bottom: 20px">
      <el-form :inline="true">
        <el-form-item label="选择员工">
          <el-select v-model="selectedEmployee" placeholder="请选择员工" filterable style="width: 200px">
            <el-option v-for="e in employees" :key="e.id" :label="e.name" :value="e.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleCheckIn" :disabled="!selectedEmployee">签到</el-button>
          <el-button type="warning" @click="handleCheckOut" :disabled="!selectedEmployee">签退</el-button>
          <el-button @click="leaveDialogVisible = true" :disabled="!selectedEmployee">请假申请</el-button>
        </el-form-item>
        <el-form-item label="日期筛选">
          <el-date-picker v-model="filterDate" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" clearable @change="loadAttendances" />
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 考勤记录 -->
    <el-card shadow="hover">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="考勤记录" name="attendance">
          <el-table :data="attendances" v-loading="loading" stripe border>
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="employee_name" label="员工" width="100" />
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column prop="check_in" label="签到时间" width="120" />
            <el-table-column prop="check_out" label="签退时间" width="120" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="statusType(row.status)" size="small">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 16px; display: flex; justify-content: flex-end">
            <el-pagination
              v-model:current-page="page"
              v-model:page-size="perPage"
              :total="total"
              :page-sizes="[10, 20]"
              layout="total, sizes, prev, pager, next"
              @size-change="loadAttendances"
              @current-change="loadAttendances"
            />
          </div>
        </el-tab-pane>
        <el-tab-pane label="请假审批" name="leave">
          <el-table :data="leaves" v-loading="leaveLoading" stripe border>
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="employee_name" label="员工" width="100" />
            <el-table-column prop="start_date" label="开始日期" width="120" />
            <el-table-column prop="end_date" label="结束日期" width="120" />
            <el-table-column prop="reason" label="原因" min-width="150" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="leaveStatusType(row.status)" size="small">{{ leaveStatusText(row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column v-if="admin" label="操作" width="160">
              <template #default="{ row }">
                <template v-if="row.status === 'pending'">
                  <el-button type="success" link @click="handleApprove(row.id, 'approved')">批准</el-button>
                  <el-button type="danger" link @click="handleApprove(row.id, 'rejected')">驳回</el-button>
                </template>
                <span v-else>已处理</span>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 请假弹窗 -->
    <el-dialog v-model="leaveDialogVisible" title="请假申请" width="500px" destroy-on-close>
      <el-form :model="leaveForm" label-width="80px">
        <el-form-item label="起止日期">
          <el-date-picker v-model="leaveDates" type="daterange" value-format="YYYY-MM-DD" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 100%" />
        </el-form-item>
        <el-form-item label="请假原因">
          <el-input v-model="leaveForm.reason" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="leaveDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleLeave">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getAttendances, checkIn, checkOut, applyLeave, getLeaves, approveLeave } from '../../api/attendance'
import { getAllEmployees } from '../../api/employee'
import { isAdmin } from '../../utils/auth'

const admin = isAdmin()

const activeTab = ref('attendance')
const selectedEmployee = ref(null)
const filterDate = ref('')
const employees = ref([])
const attendances = ref([])
const leaves = ref([])
const loading = ref(false)
const leaveLoading = ref(false)
const page = ref(1)
const perPage = ref(10)
const total = ref(0)
const leaveDialogVisible = ref(false)
const leaveDates = ref([])
const leaveForm = reactive({ reason: '' })

onMounted(() => {
  loadEmployees()
  loadAttendances()
  loadLeaves()
})

async function loadEmployees() {
  const res = await getAllEmployees()
  employees.value = res.data
}

async function loadAttendances() {
  loading.value = true
  try {
    const params = { page: page.value, per_page: perPage.value }
    if (filterDate.value) params.date = filterDate.value
    const res = await getAttendances(params)
    attendances.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

async function loadLeaves() {
  leaveLoading.value = true
  try {
    const res = await getLeaves({ page: 1, per_page: 100 })
    leaves.value = res.data.items
  } finally {
    leaveLoading.value = false
  }
}

async function handleCheckIn() {
  await checkIn(selectedEmployee.value)
  ElMessage.success('签到成功')
  loadAttendances()
}

async function handleCheckOut() {
  await checkOut(selectedEmployee.value)
  ElMessage.success('签退成功')
  loadAttendances()
}

async function handleLeave() {
  if (!leaveDates.value || leaveDates.value.length !== 2) {
    ElMessage.warning('请选择日期范围')
    return
  }
  await applyLeave({
    employee_id: selectedEmployee.value,
    start_date: leaveDates.value[0],
    end_date: leaveDates.value[1],
    reason: leaveForm.reason,
  })
  ElMessage.success('请假申请已提交')
  leaveDialogVisible.value = false
  leaveForm.reason = ''
  leaveDates.value = []
  loadLeaves()
}

async function handleApprove(id, action) {
  await approveLeave(id, action)
  ElMessage.success('操作成功')
  loadLeaves()
}

function statusType(s) {
  return { '正常': 'success', '迟到': 'warning', '早退': 'warning', '缺勤': 'danger', '请假': 'info' }[s] || ''
}

function leaveStatusType(s) {
  return { pending: 'warning', approved: 'success', rejected: 'danger' }[s] || ''
}

function leaveStatusText(s) {
  return { pending: '待审批', approved: '已批准', rejected: '已驳回' }[s] || s
}
</script>
