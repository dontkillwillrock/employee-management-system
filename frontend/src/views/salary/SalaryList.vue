<template>
  <div>
    <!-- 搜索栏 -->
    <el-card shadow="hover" style="margin-bottom: 20px">
      <el-form :inline="true" :model="queryForm">
        <el-form-item label="月份">
          <el-date-picker v-model="queryForm.month" type="month" value-format="YYYY-MM" placeholder="选择月份" clearable @change="loadData" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" placeholder="全部" clearable @change="loadData" style="width: 120px">
            <el-option label="已发放" value="已发放" />
            <el-option label="未发放" value="未发放" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="hover">
      <div style="margin-bottom: 16px">
        <el-button v-if="admin" type="primary" @click="openForm(null)">
          <el-icon><Plus /></el-icon> 新增工资记录
        </el-button>
      </div>

      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="employee_name" label="员工" width="100" />
        <el-table-column prop="month" label="月份" width="100" />
        <el-table-column prop="base_salary" label="基本工资" width="110">
          <template #default="{ row }">¥{{ row.base_salary }}</template>
        </el-table-column>
        <el-table-column prop="bonus" label="奖金" width="90">
          <template #default="{ row }">¥{{ row.bonus }}</template>
        </el-table-column>
        <el-table-column prop="deduction" label="扣款" width="90">
          <template #default="{ row }">¥{{ row.deduction }}</template>
        </el-table-column>
        <el-table-column prop="total" label="实发工资" width="110">
          <template #default="{ row }">
            <span style="font-weight: bold; color: #409eff">¥{{ row.total }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === '已发放' ? 'success' : 'warning'" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column v-if="admin" label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="openForm(row)">编辑</el-button>
            <el-button v-if="row.status === '未发放'" type="success" link @click="handlePay(row.id)">发放</el-button>
            <el-popconfirm title="确定删除？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button type="danger" link>删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin-top: 16px; display: flex; justify-content: flex-end">
        <el-pagination
          v-model:current-page="queryForm.page"
          v-model:page-size="queryForm.per_page"
          :total="total"
          :page-sizes="[10, 20]"
          layout="total, sizes, prev, pager, next"
          @size-change="loadData"
          @current-change="loadData"
        />
      </div>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑工资' : '新增工资'" width="500px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="员工" prop="employee_id">
          <el-select v-model="form.employee_id" placeholder="请选择员工" filterable style="width: 100%">
            <el-option v-for="e in employees" :key="e.id" :label="e.name" :value="e.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="月份" prop="month">
          <el-date-picker v-model="form.month" type="month" value-format="YYYY-MM" placeholder="选择月份" style="width: 100%" />
        </el-form-item>
        <el-form-item label="基本工资" prop="base_salary">
          <el-input-number v-model="form.base_salary" :min="0" :step="1000" style="width: 100%" />
        </el-form-item>
        <el-form-item label="奖金">
          <el-input-number v-model="form.bonus" :min="0" :step="100" style="width: 100%" />
        </el-form-item>
        <el-form-item label="扣款">
          <el-input-number v-model="form.deduction" :min="0" :step="100" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="未发放" value="未发放" />
            <el-option label="已发放" value="已发放" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getSalaries, createSalary, updateSalary, deleteSalary, paySalary } from '../../api/salary'
import { getAllEmployees } from '../../api/employee'
import { isAdmin } from '../../utils/auth'

const admin = isAdmin()

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const tableData = ref([])
const total = ref(0)
const employees = ref([])
const editId = ref(null)

const queryForm = reactive({ month: '', status: '', page: 1, per_page: 10 })
const form = reactive({
  employee_id: null, month: '', base_salary: 0, bonus: 0, deduction: 0, status: '未发放',
})

const rules = {
  employee_id: [{ required: true, message: '请选择员工', trigger: 'change' }],
  month: [{ required: true, message: '请选择月份', trigger: 'change' }],
  base_salary: [{ required: true, message: '请输入基本工资', trigger: 'blur' }],
}

onMounted(() => {
  loadData()
  loadEmployees()
})

async function loadData() {
  loading.value = true
  try {
    const res = await getSalaries(queryForm)
    tableData.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

async function loadEmployees() {
  const res = await getAllEmployees()
  employees.value = res.data
}

function openForm(row) {
  isEdit.value = !!row
  editId.value = row?.id || null
  Object.assign(form, row ? { ...row } : {
    employee_id: null, month: '', base_salary: 8000, bonus: 0, deduction: 0, status: '未发放',
  })
  dialogVisible.value = true
}

async function handleSubmit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateSalary(editId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createSalary(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } finally {
    submitting.value = false
  }
}

async function handlePay(id) {
  await paySalary(id)
  ElMessage.success('发放成功')
  loadData()
}

async function handleDelete(id) {
  await deleteSalary(id)
  ElMessage.success('删除成功')
  loadData()
}
</script>
