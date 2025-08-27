#!/bin/bash
# Script to download ligand SDF files from PubChem using their CIDs.
# Usage: ./fetch_ligands.sh <CID1> <CID2> ...

# The directory where SDF files will be saved
SDF_DIR="ligands/sdf"

# Create the directory if it doesn't exist
mkdir -p $SDF_DIR

# Loop through all the CIDs provided as arguments
for CID in "$@"
do
  echo "Fetching CID: $CID"
  # Construct the download URL
  URL="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/$CID/sdf?record_type=3d"
  # Download the file using curl and save it with the CID as its name
  curl -L "$URL" -o "$SDF_DIR/$CID.sdf"
done

echo "Ligand download complete."