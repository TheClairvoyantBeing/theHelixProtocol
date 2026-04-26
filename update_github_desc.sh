#!/bin/bash
# Script to update the GitHub repository description.
# Run this if you have the GitHub CLI (gh) installed and authenticated.
# Copyright (c) 2026 HELIX. All rights reserved.

echo "Updating GitHub repository description..."
gh repo edit --description "HELIX Personal Intelligence OS. Fully local, multimodal, self-improving knowledge assistant with a 3-tier memory system."
echo "Done."
