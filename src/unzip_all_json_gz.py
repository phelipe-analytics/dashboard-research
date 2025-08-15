import gzip
import shutil
from pathlib import Path

def unzip_all_json_gz(input_folder="data", output_folder="data_unzipped"):
  Path(output_folder).mkdir(parents=True, exist_ok=True)
  
  for file_path in Path(input_folder).glob("*.json.gz"):
    output_path = Path(output_folder) / file_path.with_suffix("").name

    with gzip.open(file_path, "rb") as f_in:
      with open(output_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

    print(f"Descompactado: {file_path} -> {output_path}")
    