<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <div class="stat-card card-blue" @click="$router.push('/employees')">
          <div class="stat-icon"><el-icon :size="24"><User /></el-icon></div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_employees }}</div>
            <div class="stat-label">在职员工</div>
          </div>
          <div class="stat-wave"></div>
          <el-icon class="stat-arrow"><ArrowRight /></el-icon>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card card-green" @click="$router.push('/departments')">
          <div class="stat-icon"><el-icon :size="24"><OfficeBuilding /></el-icon></div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_departments }}</div>
            <div class="stat-label">部门数量</div>
          </div>
          <div class="stat-wave"></div>
          <el-icon class="stat-arrow"><ArrowRight /></el-icon>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card card-orange" @click="$router.push('/attendances')">
          <div class="stat-icon"><el-icon :size="24"><Clock /></el-icon></div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.today_checked }}</div>
            <div class="stat-label">今日打卡</div>
          </div>
          <div class="stat-wave"></div>
          <el-icon class="stat-arrow"><ArrowRight /></el-icon>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card card-red" @click="$router.push('/attendances')">
          <div class="stat-icon"><el-icon :size="24"><WarningFilled /></el-icon></div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.today_late }}</div>
            <div class="stat-label">今日迟到</div>
          </div>
          <div class="stat-wave"></div>
          <el-icon class="stat-arrow"><ArrowRight /></el-icon>
        </div>
      </el-col>
    </el-row>

    <!-- 图表 -->
    <el-row :gutter="20" class="charts">
      <el-col :span="12">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-title"><div class="title-dot dot-blue"></div>部门人员分布</div>
          </template>
          <div ref="pieChartRef" style="height: 340px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never" class="chart-card">
          <template #header>
            <div class="card-title"><div class="title-dot dot-green"></div>薪资趋势</div>
          </template>
          <div ref="barChartRef" style="height: 340px"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 薪资统计 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card shadow="never" class="chart-card">
          <div class="salary-summary">
            <div class="salary-item">
              <div class="salary-icon paid-icon"><el-icon :size="20"><CircleCheckFilled /></el-icon></div>
              <div>
                <div class="salary-label">已发放薪资总额</div>
                <div class="salary-value paid">¥{{ formatMoney(stats.total_salary_paid) }}</div>
              </div>
            </div>
            <div class="salary-item">
              <div class="salary-icon unpaid-icon"><el-icon :size="20"><Clock /></el-icon></div>
              <div>
                <div class="salary-label">待发放薪资总额</div>
                <div class="salary-value unpaid">¥{{ formatMoney(stats.total_salary_unpaid) }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getDashboardStats } from '../api/dashboard'

const pieChartRef = ref()
const barChartRef = ref()
const stats = reactive({
  total_employees: 0,
  total_departments: 0,
  today_checked: 0,
  today_late: 0,
  dept_distribution: [],
  total_salary_paid: 0,
  total_salary_unpaid: 0,
  salary_trend: [],
})

function formatMoney(val) {
  return Number(val || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2 })
}

const colors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399']

onMounted(async () => {
  const res = await getDashboardStats()
  Object.assign(stats, res.data)
  await nextTick()
  initPieChart()
  initBarChart()
})

function initPieChart() {
  const chart = echarts.init(pieChartRef.value)
  chart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c}人 ({d}%)' },
    legend: { bottom: 0, textStyle: { color: '#999' } },
    series: [{
      type: 'pie',
      radius: ['45%', '75%'],
      label: { show: false },
      emphasis: {
        label: { show: true, fontSize: 14, fontWeight: 'bold' },
      },
      data: stats.dept_distribution.map((item, i) => ({
        ...item,
        itemStyle: { color: colors[i % colors.length] },
      })),
    }]
  })
  window.addEventListener('resize', () => chart.resize())
}

function initBarChart() {
  const chart = echarts.init(barChartRef.value)
  const trend = [...stats.salary_trend].reverse()
  chart.setOption({
    tooltip: { trigger: 'axis', formatter: p => `${p[0].name}<br/>总额: ¥${p[0].value.toLocaleString()}` },
    grid: { left: 60, right: 20, top: 20, bottom: 30 },
    xAxis: {
      type: 'category',
      data: trend.map(t => t.month),
      axisLine: { lineStyle: { color: '#eee' } },
      axisLabel: { color: '#999' },
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: '#f5f5f5' } },
      axisLabel: { color: '#999', formatter: v => `${(v / 10000).toFixed(0)}万` },
    },
    series: [{
      type: 'bar',
      data: trend.map(t => t.total),
      barWidth: 32,
      itemStyle: {
        borderRadius: [6, 6, 0, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#409eff' },
          { offset: 1, color: '#67c23a' },
        ]),
      },
    }]
  })
  window.addEventListener('resize', () => chart.resize())
}
</script>

<style scoped>
.stat-cards { margin-bottom: 20px; }

.stat-card {
  position: relative;
  border-radius: 16px;
  padding: 24px;
  color: #fff;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}
.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}
.card-blue { background: linear-gradient(135deg, #409eff, #66b1ff); }
.card-green { background: linear-gradient(135deg, #67c23a, #85ce61); }
.card-orange { background: linear-gradient(135deg, #e6a23c, #ebb563); }
.card-red { background: linear-gradient(135deg, #f56c6c, #f78989); }

.stat-icon {
  width: 44px; height: 44px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 16px;
}
.stat-value {
  font-size: 32px; font-weight: bold; margin-bottom: 4px;
}
.stat-label {
  font-size: 14px; opacity: 0.85;
}

.stat-wave {
  position: absolute;
  bottom: -10px; right: -10px;
  width: 100px; height: 100px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 50%;
  animation: wave 3s ease-in-out infinite;
}
@keyframes wave {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}

.stat-arrow {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0;
  transition: opacity 0.3s, transform 0.3s;
}
.stat-card:hover .stat-arrow {
  opacity: 0.7;
  transform: translateY(-50%) translateX(4px);
}

.chart-card {
  border-radius: 16px;
  border: 1px solid #f0f0f0;
}
.chart-card :deep(.el-card__header) {
  border-bottom: 1px solid #f5f5f5;
  padding: 16px 20px;
}
.card-title {
  display: flex; align-items: center; gap: 8px;
  font-size: 15px; font-weight: 600; color: #1a1a1a;
}
.title-dot {
  width: 8px; height: 8px; border-radius: 50%;
}
.dot-blue { background: #409eff; }
.dot-green { background: #67c23a; }

.salary-summary {
  display: flex;
  justify-content: space-around;
  padding: 16px 0;
}
.salary-item {
  display: flex; align-items: center; gap: 16px;
}
.salary-icon {
  width: 48px; height: 48px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
}
.paid-icon { background: rgba(103, 194, 58, 0.1); color: #67c23a; }
.unpaid-icon { background: rgba(230, 162, 60, 0.1); color: #e6a23c; }
.salary-label { color: #999; font-size: 13px; margin-bottom: 6px; }
.salary-value { font-size: 24px; font-weight: bold; }
.salary-value.paid { color: #67c23a; }
.salary-value.unpaid { color: #e6a23c; }
</style>
