<template>
  <div>
    <!-- 搜索栏 -->
    <el-card shadow="hover" style="margin-bottom: 20px">
      <el-form :inline="true" :model="queryForm">
        <el-form-item label="姓名">
          <el-input v-model="queryForm.name" placeholder="请输入姓名" clearable @clear="loadData" @keyup.enter="loadData" />
        </el-form-item>
        <el-form-item label="部门">
          <el-select v-model="queryForm.department_id" placeholder="全部" clearable @change="loadData" style="width: 160px">
            <el-option v-for="d in departments" :key="d.id" :label="d.name" :value="d.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" placeholder="全部" clearable @change="loadData" style="width: 120px">
            <el-option label="在职" value="在职" />
            <el-option label="离职" value="离职" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">搜索</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 操作栏 -->
    <el-card shadow="hover">
      <div style="margin-bottom: 16px">
        <el-button v-if="admin" type="primary" @click="openForm(null)">
          <el-icon><Plus /></el-icon> 新增员工
        </el-button>
      </div>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="gender" label="性别" width="70" />
        <el-table-column prop="phone" label="电话" width="140" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="position" label="职位" width="120" />
        <el-table-column prop="department_name" label="部门" width="120" />
        <el-table-column prop="hire_date" label="入职日期" width="120" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === '在职' ? 'success' : 'danger'" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="登录账号" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.user_id" type="success" size="small">已开通</el-tag>
            <el-tag v-else type="info" size="small">未开通</el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="admin" label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="openForm(row)">编辑</el-button>
            <el-button v-if="!row.user_id" type="success" link @click="openAccountForm(row)">创建账号</el-button>
            <el-popconfirm v-if="row.user_id" title="确定删除该员工的登录账号？" @confirm="handleDeleteAccount(row.id)">
              <template #reference>
                <el-button type="warning" link>删除账号</el-button>
              </template>
            </el-popconfirm>
            <el-popconfirm title="确定删除该员工？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button type="danger" link>删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div style="margin-top: 16px; display: flex; justify-content: flex-end">
        <el-pagination
          v-model:current-page="queryForm.page"
          v-model:page-size="queryForm.per_page"
          :total="total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @size-change="loadData"
          @current-change="loadData"
        />
      </div>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑员工' : '新增员工'" width="600px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="form.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="电话">
              <el-input v-model="form.phone" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱">
              <el-input v-model="form.email" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="职位">
              <el-input v-model="form.position" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="部门">
              <el-select v-model="form.department_id" placeholder="请选择部门" style="width: 100%">
                <el-option v-for="d in departments" :key="d.id" :label="d.name" :value="d.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="入职日期">
              <el-date-picker v-model="form.hire_date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-select v-model="form.status" style="width: 100%">
                <el-option label="在职" value="在职" />
                <el-option label="离职" value="离职" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 创建账号弹窗 -->
    <el-dialog v-model="accountDialogVisible" title="创建登录账号" width="400px" destroy-on-close>
      <el-form :model="accountForm" :rules="accountRules" ref="accountFormRef" label-width="80px">
        <el-form-item label="员工姓名">
          <el-input :value="accountEmployeeName" disabled />
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="accountForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="accountForm.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="accountDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="accountSubmitting" @click="handleCreateAccount">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getEmployees, createEmployee, updateEmployee, deleteEmployee, createEmployeeAccount, deleteEmployeeAccount } from '../../api/employee'
import { getDepartments } from '../../api/department'
import { isAdmin } from '../../utils/auth'

const admin = isAdmin()
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const tableData = ref([])
const total = ref(0)
const departments = ref([])
const editId = ref(null)

const queryForm = reactive({ name: '', department_id: null, status: '', page: 1, per_page: 10 })
const form = reactive({
  name: '', gender: '男', phone: '', email: '', position: '',
  department_id: null, hire_date: '', status: '在职',
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
}

const accountDialogVisible = ref(false)
const accountSubmitting = ref(false)
const accountFormRef = ref()
const accountEmployeeId = ref(null)
const accountEmployeeName = ref('')
const accountForm = reactive({ username: '', password: '' })
const accountRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '密码至少6位', trigger: 'blur' }],
}

onMounted(() => {
  loadData()
  loadDepartments()
})

async function loadData() {
  loading.value = true
  try {
    const res = await getEmployees(queryForm)
    tableData.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

async function loadDepartments() {
  const res = await getDepartments()
  departments.value = res.data
}

function resetQuery() {
  Object.assign(queryForm, { name: '', department_id: null, status: '', page: 1 })
  loadData()
}

function openForm(row) {
  isEdit.value = !!row
  editId.value = row?.id || null
  Object.assign(form, row ? { ...row } : {
    name: '', gender: '男', phone: '', email: '', position: '',
    department_id: null, hire_date: '', status: '在职',
  })
  dialogVisible.value = true
}

async function handleSubmit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateEmployee(editId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createEmployee(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(id) {
  await deleteEmployee(id)
  ElMessage.success('删除成功')
  loadData()
}

function openAccountForm(row) {
  accountEmployeeId.value = row.id
  accountEmployeeName.value = row.name
  accountForm.username = row.phone || ''
  accountForm.password = ''
  accountDialogVisible.value = true
}

async function handleCreateAccount() {
  await accountFormRef.value.validate()
  accountSubmitting.value = true
  try {
    await createEmployeeAccount(accountEmployeeId.value, { ...accountForm })
    ElMessage.success('账号创建成功')
    accountDialogVisible.value = false
    loadData()
  } finally {
    accountSubmitting.value = false
  }
}

async function handleDeleteAccount(employeeId) {
  await deleteEmployeeAccount(employeeId)
  ElMessage.success('账号删除成功')
  loadData()
}
</script>
