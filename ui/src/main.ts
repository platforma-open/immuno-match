import { BlockLayout } from '@platforma-sdk/ui-vue';
import '@platforma-sdk/ui-vue/styles';
import '@milaboratories/graph-maker/styles';
import { createApp } from 'vue';
import { sdkPlugin } from './app';

createApp(BlockLayout).use(sdkPlugin).mount('#app');
