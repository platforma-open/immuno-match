import type { GraphMakerState } from '@milaboratories/graph-maker';
import type {
  InferOutputsType,
  PlRef,
} from '@platforma-sdk/model';
import {
  BlockModel,
  createPFrameForGraphs,
  isPColumnSpec,
} from '@platforma-sdk/model';

export type BlockArgs = {
  // Heavy chain PColumn reference from a MiXCR Clonotyping 2 block
  // It will be used to get the associated heavy chain sequences, light chain sequences,
  // and light chain type
  inputHeavy?: PlRef;
};

// Persisted UI state and initial graph configuration
export type UiState = {
  graphStateHistogram: GraphMakerState;
};

export const model = BlockModel.create()

  .withArgs<BlockArgs>({})

  // Activate "Run" button only after these conditions get fulfilled
  .argsValid((ctx) => ctx.args.inputHeavy !== undefined)

  .withUiState<UiState>({
    graphStateHistogram: {
      title: 'ImmunoMatch',
      template: 'bins',
      currentTab: 'settings',
      layersSettings: {
        bins: { fillColor: '#99e099' },
      },
    },
  })
  // This is used to populate the "Heavy Chain" dropdown in the UI.
  .output('heavyInputOptions', (ctx) => {
    return ctx.resultPool.getOptions(
      (spec) =>
        isPColumnSpec(spec)
        && spec.name === 'pl7.app/vdj/sequence'
        && spec.domain?.['pl7.app/alphabet'] === 'aminoacid'
        && spec.domain?.['pl7.app/vdj/feature'] === 'VDJRegion'
        && spec.axesSpec?.[0]?.domain?.['pl7.app/vdj/receptor'] === 'IG'
        && spec.domain?.['pl7.app/vdj/scClonotypeChain'] === 'A'
        && spec.domain?.['pl7.app/vdj/scClonotypeChain/index'] === 'primary',
    );
  })

  .output('log', (ctx) => ctx.outputs?.resolve('log')?.getLogHandle())

  // Get the IMM predictions and prepare them for the histogram graph
  .output('predictions', (ctx) => {
    const pCols = ctx.outputs?.resolve('predictions')?.getPColumns();
    if (pCols === undefined) return undefined;

    return createPFrameForGraphs(ctx, pCols);
  })

  .output('isRunning', (ctx) => ctx.outputs?.getIsReadyOrError() === false)

  // Create the UI sections
  .sections((_ctx) => [
    { type: 'link', href: '/', label: 'Main' },
  ])

  .done(2);

export type BlockOutputs = InferOutputsType<typeof model>;
