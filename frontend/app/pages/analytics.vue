<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line, Bar } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const history = ref<any[]>([])
const loading = ref(true)

const lineChartData = ref<any>({
  labels: [],
  datasets: []
})

const barChartData = ref<any>({
  labels: [],
  datasets: []
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}

const config = useRuntimeConfig()

const fetchData = async () => {
  try {
    const response = await fetch(`${config.public.apiUrl}/history`)
    const data = await response.json()
    history.value = data
    processData(data)
  } catch (e) {
    console.error("Failed to fetch history", e)
  } finally {
    loading.value = false
  }
}

const processData = (data: any[]) => {
  const labels = data.map((item, index) => `Test ${index + 1}`)
  
  lineChartData.value = {
    labels,
    datasets: [
      {
        label: 'DEI Score',
        backgroundColor: '#4f46e5',
        borderColor: '#4f46e5',
        data: data.map(item => item.dei)
      }
    ]
  }

  barChartData.value = {
    labels,
    datasets: [
      {
        label: 'Robustness Score',
        backgroundColor: '#10b981',
        data: data.map(item => item.input.robustness_score)
      },
      {
        label: 'Error Rate (%)',
        backgroundColor: '#ef4444',
        data: data.map(item => item.input.error_rate * 100)
      }
    ]
  }
}

const resetHistory = async () => {
    if(!confirm("Are you sure you want to clear history?")) return;
    try {
        await fetch(`${config.public.apiUrl}/reset`, { method: 'POST' })
        fetchData()
    } catch(e) {
        console.error(e)
    }
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="space-y-8">
    <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>
        <button @click="resetHistory" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm">Clear History</button>
    </div>

    <div v-if="loading" class="text-center py-12">
      <p class="text-gray-500">Loading data...</p>
    </div>

    <div v-else-if="history.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <p class="text-gray-500">No data available. Run some tests on the Home page first.</p>
      <NuxtLink to="/" class="mt-4 inline-block text-indigo-600 hover:text-indigo-500">Go to Calculator &rarr;</NuxtLink>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="bg-white p-6 rounded-lg shadow h-96">
        <h3 class="text-lg font-medium text-gray-900 mb-4">DEI Trend</h3>
        <Line :data="lineChartData" :options="chartOptions" />
      </div>

      <div class="bg-white p-6 rounded-lg shadow h-96">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Robustness vs Error Rate</h3>
        <Bar :data="barChartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>
