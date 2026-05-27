<template>
  <div>
    <el-card shadow="hover">
      <div style="margin-bottom: 16px">
        <el-button v-if="admin" type="primary" @click="openForm(null)">
          <el-icon><Plus /></el-icon> 新增部门
        </el-button>
      </div>

      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="部门名称" width="180" />
        <el-table-column prop="description" label="部门描述" min-width="200" />
        <el-table-column prop="employee_count" label="员工数量" width="100" align="center" />
        <el-table-column v-if="admin" label="操作" width="180">
          <template #default="{ row }">
            <el-button type="primary" link @click="openForm(row)">编辑</el-button>
            <el-popconfirm title="确定删除该部门？" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button type="danger" link>删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑部门' : '新增部门'" width="500px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
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
import { getDepartments, createDepartment, updateDepartment, deleteDepartment } from '../../api/department'
import { isAdmin } from '../../utils/auth'

const admin = isAdmin()

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()
const tableData = ref([])
const editId = ref(null)

const form = reactive({ name: '', description: '' })
const rules = { name: [{ required: true, message: '请输入部门名称', trigger: 'blur' }] }

onMounted(() => loadData())

async function loadData() {
  loading.value = true
  try {
    const res = await getDepartments()
    tableData.value = res.data
  } finally {
    loading.value = false
  }
}

function openForm(row) {
  isEdit.value = !!row
  editId.value = row?.id || null
  Object.assign(form, row ? { name: row.name, description: row.description } : { name: '', description: '' })
  dialogVisible.value = true
}

async function handleSubmit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateDepartment(editId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createDepartment(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(id) {
  await deleteDepartment(id)
  ElMessage.success('删除成功')
  loadData()
}
</script>
