<script setup lang="ts">
import { PlDropdownRef } from '@platforma-sdk/ui-vue';
import { GraphMaker } from '@milaboratories/graph-maker';
import type { PredefinedGraphOption } from '@milaboratories/graph-maker';
import { useApp } from '../app';
import { watch } from 'vue';

const app = useApp();

watch(() => app.model.args.inputHeavy, (newVal) => {
  if (newVal === undefined) {
    app.model.ui.graphStateHistogram.currentTab = 'settings';
  }
}, { immediate: true });

</script>

<template>
  <GraphMaker
    v-model="app.model.ui.graphStateHistogram"
    chartType="histogram"
    :p-frame="app.model.outputs.predictions"
    :default-options="[{
      inputName: 'value',
      selectedSource: {
        kind: 'PColumn',
        name: 'pl7.app/immunomatch/pairing_score',
        valueType: 'Double',
        axesSpec: [
          {
            name: 'pl7.app/vdj/scClonotypeKey',
            type: 'String',
          },
        ],
      },
    }] satisfies PredefinedGraphOption<'histogram'>[]"
  >
    <template #settingsSlot>
      <PlDropdownRef v-model="app.model.args.inputHeavy" :options="app.model.outputs.heavyInputOptions" label="Heavy Input" />
    </template>
  </GraphMaker>
</template>
