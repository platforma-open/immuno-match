<script setup lang="ts">
import {
  PlBlockPage,
  PlBtnGhost,
  PlDropdownRef,
  PlMaskIcon24,
  PlSlideModal,
} from '@platforma-sdk/ui-vue';
import { GraphMaker } from '@milaboratories/graph-maker';
import type { PredefinedGraphOption } from '@milaboratories/graph-maker';
import { useApp } from '../app';
import { ref } from 'vue';

const app = useApp();
const settingsAreOpen = ref(app.model.args.inputHeavy === undefined);

</script>

<template>
  <PlBlockPage>
    <template #title>ImmunoMatch</template>
    <template #append>
      <PlBtnGhost @click.stop="() => settingsAreOpen = true">
        Settings
        <template #append>
          <PlMaskIcon24 name="settings" />
        </template>
      </PlBtnGhost>
    </template>

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
    />
  </PlBlockPage>

  <PlSlideModal v-model="settingsAreOpen">
    <template #title>Settings</template>
    <PlDropdownRef v-model="app.model.args.inputHeavy" :options="app.model.outputs.heavyInputOptions" label="Heavy Input" />
  </PlSlideModal>
</template>
