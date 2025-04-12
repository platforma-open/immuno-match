# Description

Block description is [here](docs/description.md)

# Block Exports

The block exports a single PColumn to the ResultPool that contains the
ImmunoMatch pairing scores.
The axes are identical to those of the primary Heavy chain PColumn of th
MiXCR Clonotyping 2 block.

```json
{
  "annotations": {
    "pl7.app/label": "Pairing Score",
    "pl7.app/vdj/receptor": "IG"
  },
  "axesSpec": [
    {
      "annotations": {
        "pl7.app/label": "Clone label",
        "pl7.app/segmentedBy": "[\"pl7.app/vdj/clonotypingRunId\"]",
        "pl7.app/table/orderPriority": "110000",
        "pl7.app/table/visibility": "optional"
      },
      "domain": {
        "pl7.app/vdj/clonotypingRunId": <mixcr-runId>,
        "pl7.app/vdj/receptor": "IG",
        "pl7.app/vdj/scClonotypeKey/structure": "[[\"pl7.app/vdj/sequence\",[\"pl7.app/alphabet\",\"nucleotide\"],[\"pl7.app/vdj/feature\",\"VDJRegion\"]],[\"pl7.app/vdj/geneHit\",[\"pl7.app/vdj/reference\",\"VGene\"]],[\"pl7.app/vdj/geneHit\",[\"pl7.app/vdj/reference\",\"JGene\"]]]"
      },
      "name": "pl7.app/vdj/scClonotypeKey",
      "type": "String"
    }
  ],
  "domain": {
    "pl7.app/alphabet": "aminoacid",
    "pl7.app/blockId": <blockId>,
    "pl7.app/vdj/feature": "VDJRegion",
    "pl7.app/vdj/scClonotypeChain/index": "primary"
  },
  "kind": "PColumn",
  "name": "pl7.app/immunomatch/pairing_score",
  "valueType": "Double"
}
```
