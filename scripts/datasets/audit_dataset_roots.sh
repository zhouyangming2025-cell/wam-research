#!/usr/bin/env bash
set -u

# Lightweight inventory for existing nuPlan / OpenScene / NAVSIM assets.
#
# Usage:
#   bash scripts/datasets/audit_dataset_roots.sh /path/to/OpenScene /path/to/nuPlan
#
# This script intentionally avoids recursively hashing multi-TB trees.
# It uses directory existence checks + du at the asset boundary that matters for
# download decisions.

OPENSCENE_ROOT="${1:-}"
NUPLAN_ROOT="${2:-}"

if [[ -z "$OPENSCENE_ROOT" || -z "$NUPLAN_ROOT" ]]; then
  echo "Usage: $0 <OPENSCENE_ROOT> <NUPLAN_ROOT>"
  exit 2
fi

size_if_exists() {
  local label="$1"
  local path="$2"
  if [[ -e "$path" ]]; then
    printf "%-42s " "$label"
    du -sh "$path" 2>/dev/null | awk '{print $1}'
  else
    printf "%-42s %s\n" "$label" "MISSING"
  fi
}

count_db() {
  local label="$1"
  local path="$2"
  if [[ -d "$path" ]]; then
    local n
    n=$(find "$path" -maxdepth 1 -type f -name '*.db' 2>/dev/null | wc -l)
    printf "%-42s %s DB files\n" "$label" "$n"
  else
    printf "%-42s %s\n" "$label" "MISSING"
  fi
}

echo "============================================================"
echo "OpenScene / NAVSIM inventory"
echo "root: $OPENSCENE_ROOT"
echo "============================================================"

# OpenScene native layout.
size_if_exists "openscene-v1.1/meta_datas/trainval" "$OPENSCENE_ROOT/openscene-v1.1/meta_datas/trainval"
size_if_exists "openscene-v1.1/sensor_blobs/trainval" "$OPENSCENE_ROOT/openscene-v1.1/sensor_blobs/trainval"
size_if_exists "openscene-v1.1/meta_datas/test" "$OPENSCENE_ROOT/openscene-v1.1/meta_datas/test"
size_if_exists "openscene-v1.1/sensor_blobs/test" "$OPENSCENE_ROOT/openscene-v1.1/sensor_blobs/test"

# NAVSIM-reorganized layout.
size_if_exists "navsim_logs/trainval" "$OPENSCENE_ROOT/navsim_logs/trainval"
size_if_exists "sensor_blobs/trainval" "$OPENSCENE_ROOT/sensor_blobs/trainval"
size_if_exists "navsim_logs/test" "$OPENSCENE_ROOT/navsim_logs/test"
size_if_exists "sensor_blobs/test" "$OPENSCENE_ROOT/sensor_blobs/test"
size_if_exists "trainval_navsim_logs" "$OPENSCENE_ROOT/trainval_navsim_logs"
size_if_exists "trainval_sensor_blobs" "$OPENSCENE_ROOT/trainval_sensor_blobs"
size_if_exists "navhard_two_stage" "$OPENSCENE_ROOT/navhard_two_stage"
size_if_exists "warmup_two_stage" "$OPENSCENE_ROOT/warmup_two_stage"
size_if_exists "private_test_hard_two_stage" "$OPENSCENE_ROOT/private_test_hard_two_stage"

echo
echo "Top-level OpenScene/NAVSIM children:"
find "$OPENSCENE_ROOT" -mindepth 1 -maxdepth 2 -type d 2>/dev/null | sort | head -n 120

echo
echo "============================================================"
echo "nuPlan inventory"
echo "root: $NUPLAN_ROOT"
echo "============================================================"

size_if_exists "maps" "$NUPLAN_ROOT/maps"
size_if_exists "nuplan-v1.1/splits/trainval" "$NUPLAN_ROOT/nuplan-v1.1/splits/trainval"
size_if_exists "nuplan-v1.1/splits/test" "$NUPLAN_ROOT/nuplan-v1.1/splits/test"
size_if_exists "nuplan-v1.1/splits/mini" "$NUPLAN_ROOT/nuplan-v1.1/splits/mini"
size_if_exists "nuplan-v1.1/sensor_blobs" "$NUPLAN_ROOT/nuplan-v1.1/sensor_blobs"

count_db "trainval DB count" "$NUPLAN_ROOT/nuplan-v1.1/splits/trainval"
count_db "test DB count" "$NUPLAN_ROOT/nuplan-v1.1/splits/test"
count_db "mini DB count" "$NUPLAN_ROOT/nuplan-v1.1/splits/mini"

echo
echo "Sample sensor-log channel layout (first log only):"
SENSOR_ROOT="$NUPLAN_ROOT/nuplan-v1.1/sensor_blobs"
if [[ -d "$SENSOR_ROOT" ]]; then
  first_log=$(find "$SENSOR_ROOT" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort | head -n 1 || true)
  if [[ -n "$first_log" ]]; then
    echo "log: $first_log"
    find "$first_log" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort
  else
    echo "No extracted sensor log directory found."
  fi
else
  echo "sensor_blobs MISSING"
fi

echo
echo "============================================================"
echo "Interpretation hints"
echo "============================================================"
cat <<'EOF'
- Full OpenScene trainval sensors are officially >2000 GB.
- NAVSIM navtrain-only sensors are ~445 GB with history, ~300 GB without history.
- If full OpenScene trainval is already present, do NOT download navtrain sensors again.
- Missing nuPlan trainval DB is not by itself a blocker for NAVSIM/OpenScene WAMs.
- Do not start raw nuPlan camera/LiDAR downloads from this output alone; first build
  the public S3 manifest and bind the download to a concrete model recipe.
EOF
