<script setup lang="ts">
import type { PredefinedGraphOption } from '@milaboratories/graph-maker';
import { GraphMaker } from '@milaboratories/graph-maker';
import { PlBtnGhost, PlDropdownRef, PlLogView, PlSlideModal } from '@platforma-sdk/ui-vue';
import { ref, watch } from 'vue';
import { useApp } from '../app';

const app = useApp();

const defaultOptions: PredefinedGraphOption<'histogram'>[] = [{
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
}];
const logsOpen = ref(false);

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
    :default-options="defaultOptions"
  >
    <template #titleLineSlot>
      <PlBtnGhost @click.stop="logsOpen = true">Show logs</PlBtnGhost>
    </template>
    <template #settingsSlot>
      <PlDropdownRef v-model="app.model.args.inputHeavy" :options="app.model.outputs.heavyInputOptions" label="Heavy Input" />
    </template>
  </GraphMaker>
  <PlSlideModal v-model="logsOpen" width="800px" closeOnOutsideClick>
    <template #title>Logs</template>
    <PlLogView :log-handle="app.model.outputs.log" />
  </PlSlideModal>
</template>
