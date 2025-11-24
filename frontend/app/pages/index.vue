<script setup lang="ts">
import { ref } from 'vue'

const decisionTime = ref<number | null>(null)
const errorRate = ref<number | null>(null)
const robustnessScore = ref<number | null>(null)
const result = ref<any>(null)
const loading = ref(false)
const error = ref<string | null>(null)

const calculateDEI = async () => {
  if (!decisionTime.value || !errorRate.value || !robustnessScore.value) {
    error.value = "Please fill in all fields"
    return
  }

  loading.value = true
  error.value = null
  result.value = null

  try {
    const response = await fetch('http://localhost:8000/compute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        decision_time: decisionTime.value,
        error_rate: errorRate.value,
        robustness_score: robustnessScore.value,
      }),
    })

    if (!response.ok) {
      throw new Error('Failed to calculate DEI')
    }

    result.value = await response.json()
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">Calculate DEI</h3>
        <p class="mt-1 max-w-2xl text-sm text-gray-500">Enter the parameters to compute the Decision Efficiency Index.</p>
      </div>
      <div class="border-t border-gray-200 px-4 py-5 sm:p-6">
        <form @submit.prevent="calculateDEI" class="space-y-6">
          <div>
            <label for="decision_time" class="block text-sm font-medium text-gray-700">Decision Time (seconds)</label>
            <div class="mt-1">
              <input type="number" step="0.1" id="decision_time" v-model="decisionTime" class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border" placeholder="e.g. 2.5" required />
            </div>
          </div>

          <div>
            <label for="error_rate" class="block text-sm font-medium text-gray-700">Error Rate (0.0 - 1.0)</label>
            <div class="mt-1">
              <input type="number" step="0.01" min="0" max="1" id="error_rate" v-model="errorRate" class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border" placeholder="e.g. 0.15" required />
            </div>
          </div>

          <div>
            <label for="robustness_score" class="block text-sm font-medium text-gray-700">Robustness Score (0 - 100)</label>
            <div class="mt-1">
              <input type="number" step="1" id="robustness_score" v-model="robustnessScore" class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border" placeholder="e.g. 85" required />
            </div>
          </div>

          <div>
            <button type="submit" :disabled="loading" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-indigo-300">
              {{ loading ? 'Calculating...' : 'Run DEI Test' }}
            </button>
          </div>
        </form>

        <div v-if="error" class="mt-4 bg-red-50 border-l-4 border-red-400 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <!-- Heroicon name: solid/exclamation -->
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">
                {{ error }}
              </p>
            </div>
          </div>
        </div>

        <div v-if="result" class="mt-6 bg-green-50 border-l-4 border-green-400 p-4">
          <div class="flex">
             <div class="flex-shrink-0">
              <!-- Heroicon name: solid/check-circle -->
              <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-green-800">Result Calculated</h3>
              <div class="mt-2 text-sm text-green-700">
                <p class="text-2xl font-bold">DEI: {{ result.dei.toFixed(4) }}</p>
                <p class="mt-1">Timestamp: {{ new Date(result.timestamp).toLocaleString() }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>