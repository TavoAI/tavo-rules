#!/bin/bash
# package-bundle.sh - Package TavoAI bundles for distribution
#
# This script packages rule bundles into distributable .tavoai-bundle files
# that can be downloaded from GitHub or the Registry API.
#
# Usage:
#   ./package-bundle.sh <bundle-name> [output-dir]
#   ./package-bundle.sh --all [output-dir]
#   ./package-bundle.sh --help

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
BUNDLES_DIR="$REPO_ROOT/bundles"
OUTPUT_DIR="${2:-$REPO_ROOT/dist}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}" >&2
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}" >&2
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}" >&2
}

log_error() {
    echo -e "${RED}❌ $1${NC}" >&2
}

validate_bundle() {
    local bundle_dir="$1"
    local bundle_name="$2"

    log_info "Validating bundle: $bundle_name"

    # Check if bundle directory exists
    if [[ ! -d "$bundle_dir" ]]; then
        log_error "Bundle directory not found: $bundle_dir"
        return 1
    fi

    # Check for manifest.json
    local manifest_file="$bundle_dir/manifest.json"
    if [[ ! -f "$manifest_file" ]]; then
        log_error "Manifest file not found: $manifest_file"
        return 1
    fi

    # Validate manifest JSON
    if ! jq empty "$manifest_file" 2>/dev/null; then
        log_error "Invalid JSON in manifest: $manifest_file"
        return 1
    fi

    # Extract bundle ID and version from manifest
    local bundle_id=$(jq -r '.id' "$manifest_file")
    local version=$(jq -r '.version' "$manifest_file")

    if [[ "$bundle_id" == "null" || -z "$bundle_id" ]]; then
        log_error "Bundle ID not found in manifest"
        return 1
    fi

    if [[ "$version" == "null" || -z "$version" ]]; then
        log_error "Version not found in manifest"
        return 1
    fi

    log_success "Bundle validation passed: $bundle_id v$version"
    echo "$bundle_id:$version"
}

package_bundle() {
    local bundle_dir="$1"
    local bundle_name="$2"

    log_info "Packaging bundle: $bundle_name"

    # Validate bundle first
    local bundle_info
    if ! bundle_info=$(validate_bundle "$bundle_dir" "$bundle_name"); then
        return 1
    fi

    # Parse bundle info
    IFS=':' read -r bundle_id version <<< "$bundle_info"

    # Create output directory
    mkdir -p "$OUTPUT_DIR"

    # Create temporary directory for packaging
    local temp_dir
    temp_dir=$(mktemp -d)
    trap "rm -rf '$temp_dir'" EXIT

    local bundle_temp_dir="$temp_dir/bundle"
    mkdir -p "$bundle_temp_dir"

    # Copy manifest
    cp "$bundle_dir/manifest.json" "$bundle_temp_dir/"

    # Copy all artifacts listed in manifest
    local artifacts
    artifacts=$(jq -r '.artifacts[]' "$bundle_dir/manifest.json" 2>/dev/null || echo "")

    for artifact in $artifacts; do
        local artifact_path="$bundle_dir/$artifact"
        if [[ -f "$artifact_path" ]]; then
            # Create subdirectories if needed
            local artifact_dir
            artifact_dir=$(dirname "$bundle_temp_dir/$artifact")
            mkdir -p "$artifact_dir"

            cp "$artifact_path" "$bundle_temp_dir/$artifact"
            log_info "Added artifact: $artifact"
        else
            log_warning "Artifact not found: $artifact_path"
        fi
    done

    # Copy optional files
    local optional_files=("README.md" "CHANGELOG.md" "LICENSE")
    for optional_file in "${optional_files[@]}"; do
        if [[ -f "$bundle_dir/$optional_file" ]]; then
            cp "$bundle_dir/$optional_file" "$bundle_temp_dir/"
            log_info "Added optional file: $optional_file"
        fi
    done

    # Create bundle archive
    local bundle_filename="${bundle_id}-${version}.tavoai-bundle"
    local bundle_path="$OUTPUT_DIR/$bundle_filename"

    log_info "Creating bundle archive: $bundle_filename"
    if (cd "$temp_dir" && zip -r "$bundle_path" "bundle/" >/dev/null 2>&1); then
        # Verify the file was created
        if [[ -f "$bundle_path" ]]; then
            log_success "Bundle archive created successfully"
        else
            log_error "Bundle archive was not created"
            return 1
        fi
    else
        log_error "Failed to create bundle archive"
        return 1
    fi

    # Calculate bundle size
    local bundle_size
    bundle_size=$(du -h "$bundle_path" | cut -f1)

    log_success "Bundle packaged successfully: $bundle_filename ($bundle_size)"

    # Output bundle info for automation
    echo "$bundle_path:$bundle_size"
}

package_all_bundles() {
    local output_dir="$1"
    local total_bundles=0
    local success_count=0

    log_info "Packaging all bundles..."

    # Find all bundle directories (those with manifest.json)
    while IFS= read -r bundle_dir; do
        local bundle_name
        bundle_name=$(basename "$bundle_dir")
        total_bundles=$((total_bundles + 1))

        log_info "Processing bundle: $bundle_name"

        if package_bundle "$bundle_dir" "$bundle_name" >/dev/null 2>&1; then
            success_count=$((success_count + 1))
            log_success "Packaged: $bundle_name"
        else
            log_error "Failed to package: $bundle_name"
        fi

    done < <(find "$BUNDLES_DIR" -name "manifest.json" -exec dirname {} \;)

    log_info "Packaging complete: $success_count/$total_bundles bundles packaged"

    if [[ $success_count -eq $total_bundles ]]; then
        log_success "All bundles packaged successfully!"
    else
        log_warning "Some bundles failed to package. Check output above."
    fi
}

show_usage() {
    cat << EOF
Usage: $0 <bundle-name> [output-dir]
       $0 --all [output-dir]
       $0 --help

Package TavoAI rule bundles for distribution.

Arguments:
  bundle-name    Name of the bundle to package (e.g., 'owasp-llm-pro')
  output-dir     Directory to save packaged bundles (default: ./dist)
  --all          Package all bundles
  --help         Show this help message

Examples:
  $0 owasp-llm-pro                    # Package single bundle
  $0 owasp-llm-pro /tmp/bundles       # Package to custom directory
  $0 --all                            # Package all bundles
  $0 --all ./release                  # Package all to release directory

Output:
  Creates .tavoai-bundle files containing:
  - manifest.json (bundle metadata)
  - All rule artifacts listed in manifest
  - Optional README.md, CHANGELOG.md, LICENSE files
EOF
}

main() {
    # Check dependencies
    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed. Please install jq."
        exit 1
    fi

    if ! command -v zip &> /dev/null; then
        log_error "zip is required but not installed. Please install zip."
        exit 1
    fi

    case "${1:-}" in
        --help|-h)
            show_usage
            exit 0
            ;;
        --all)
            package_all_bundles "${2:-$OUTPUT_DIR}"
            ;;
        "")
            log_error "Bundle name required. Use --help for usage."
            exit 1
            ;;
        *)
            local bundle_name="$1"
            local bundle_dir="$BUNDLES_DIR/$bundle_name"

            if [[ ! -d "$bundle_dir" ]]; then
                log_error "Bundle not found: $bundle_name"
                log_info "Available bundles:"
                find "$BUNDLES_DIR" -name "manifest.json" -exec dirname {} \; | xargs -n1 basename | sort
                exit 1
            fi

            package_bundle "$bundle_dir" "$bundle_name"
            ;;
    esac
}

main "$@"
