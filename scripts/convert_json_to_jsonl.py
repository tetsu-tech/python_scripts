import json
import os

# フォルダのパスを指定
folder_path = './input'
out_folder_path = './output'
out_filename = 'all_data.jsonl'

# 抽出したいフィールド名のリスト
desired_fields = ['jsonPayload.custom', 'timestamp']

# ファイルを開いて追記モードで開く
with open(os.path.join(out_folder_path, out_filename), 'w') as jsonl_output:
    # フォルダ内のファイルに対してループ処理
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            if filename == '.gitkeep':
                print('ignore: ', filename)
                break

            print("ファイル名:", filename)
            with open(os.path.join(folder_path, filename), 'r') as f:
                json_data = json.load(f)
                
                ## 必要なネストしたフィールドを抽出して新しいエントリを作成し、ファイルに追記
                for entry in json_data:
                    filtered_entry = {}
                    for field_path in desired_fields:
                        # keyを下っていく
                        keys = field_path.split('.')
                        value = entry
                        for key in keys:
                            if key in value:
                                value = value[key]
                            else:
                                break
                        # .が入るとBQのフィールドでエラーになるので置換
                        new_field_path = field_path.replace('.', '_')
                        filtered_entry[new_field_path] = value
                    
                    # jsonlファイルに書き込み
                    json.dump(filtered_entry, jsonl_output)
                    jsonl_output.write('\n')
