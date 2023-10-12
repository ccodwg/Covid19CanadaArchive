#!/bin/bash
# check if datasets.json exists and exit if not
if [ ! -f datasets.json ]; then
    echo "datasets.json does not exist. Please run from the same directory as datasets.json."
    exit 1
fi

# input: file group metadata
read -p "Parent directory: " dir_parent
read -p "Meta URL: " meta_url
read -p "Meta URL name: " meta_url_name
read -p "Meta group 1: " meta_group_1
read -p "Meta group 2 (leave blank for none): " meta_group_2

# define function: input individual dataset info
function input_dataset() {
    # input: individual dataset info
    read -p "Meta name: " meta_name
    read -p "Active (y/n): " active
    # check validity of active
    while [ "$active" != "y" ] && [ "$active" != "n" ]; do
        echo "Invalid input. Please enter 'y' or 'n'."
        read -p "Active: " active
    done
    if [ "$active" = "y" ]; then
        active="True"
        active_key="active"
    else
        active="False"
        active_key="inactive"
    fi
    read -p "URL: " url
    read -p "File directory: " dir_file
    read -p "File name: " file_name
    # replace spaces in file name with underscores
    if [[ "$file_name" == *" "* ]]; then
        file_name="${file_name// /_}"
        echo "Spaces in file name have been replaced with underscores."
    fi
    read -p "File extension: " file_ext
    # derived variables
    if [ "$file_ext" = "html" ]; then
        dl_fun="html_page"
    else
        dl_fun="dl_file"
    fi
    id_name="${dir_parent^^} - ${meta_url_name} - ${meta_name}"
    if [ "$file_ext" = "html" ]; then
        id_name="{$id_name} (webpage)"
    fi
    # generate UUID
    uuid=$(uuidgen --random)
    # create JSON entry
    # create metadata
    metadata=$(jq \
        --arg meta_name "$meta_name" \
        --arg meta_url "$meta_url" \
        --arg meta_url_name "$meta_url_name" \
        --arg meta_group_1 "$meta_group_1" \
        '. | .["meta_name"]=$meta_name |
            .["meta_url"]=$meta_url |
            .["meta_url_name"]=$meta_url_name |
            .["meta_licence"]="" |
            .["meta_licence_url"]="" |
            .["meta_group_1"]=$meta_group_1' \
        <<<'{}'
    )
    # append meta_group_2 to metadata if it is not blank
    if [ "$meta_group_2" != "" ]; then
        metadata=$(jq \
            --arg meta_group_2 "$meta_group_2" \
            '. | .["meta_group_2"]=$meta_group_2' \
            <<<$metadata
        )
    fi
    # create rest of JSON entry
    json=$(jq \
        --arg id_name "$id_name" \
        --arg uuid "$uuid" \
        --arg active "$active" \
        --arg url "$url" \
        --arg dir_parent "$dir_parent" \
        --arg dir_file "$dir_file" \
        --arg file_name "$file_name" \
        --arg file_ext "$file_ext" \
        --arg dl_fun "$dl_fun" \
        --argjson metadata "$metadata" \
        '. | .["id_name"]=$id_name |
            .["uuid"]=$uuid |
            .["active"]=$active |
            .["url"]=$url |
            .["dir_parent"]=$dir_parent |
            .["dir_file"]=$dir_file |
            .["file_name"]=$file_name |
            .["file_ext"]=$file_ext |
            .["dl_fun"]=$dl_fun |
            .["args"]={} |
            .["supplementary"]={} |
            .["metadata"]=$metadata |
            .["notes"]={}' \
        <<<'{}'
    )
    echo "$json"
    # append JSON entry to datasets.json using active and dir_parents keys
    jq --argjson json "$json" \
        --arg active_key "$active_key" \
        --arg dir_parent "$dir_parent" \
        '.[$active_key][$dir_parent] += [$json]' datasets.json > datasets.json.tmp && mv datasets.json.tmp datasets.json
}

# run function and then prompt to add another dataset or exit
input_dataset
while true; do
    read -p "Add another dataset to this file group? (y/n): " yn
    case $yn in
        [Yy]* ) input_dataset;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
