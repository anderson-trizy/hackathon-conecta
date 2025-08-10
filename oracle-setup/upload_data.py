#!/usr/bin/env python3
"""
Script para upload de dados para Oracle Object Storage
"""

import oci
import json
from pathlib import Path

def upload_to_oci():
    """Upload consolidated_datasource.json para OCI Object Storage"""
    
    # Configuração OCI - usar config local primeiro, depois padrão
    config_path = Path(__file__).parent.parent / ".oci" / "config"
    
    try:
        if config_path.exists():
            print(f"📄 Usando configuração local: {config_path}")
            config = oci.config.from_file(str(config_path))
        else:
            print("📄 Usando configuração padrão ~/.oci/config")
            config = oci.config.from_file()
        
        object_storage = oci.object_storage.ObjectStorageClient(config)
    except Exception as e:
        print(f"❌ Erro ao carregar configuração OCI: {e}")
        return False
    
    # Parâmetros do bucket
    namespace = object_storage.get_namespace().data
    bucket_name = "nstech-recommendation-data"
    
    # Arquivo para upload
    data_file = Path("../data/consolidated_datasource.json")
    
    if not data_file.exists():
        print("❌ Arquivo consolidated_datasource.json não encontrado!")
        return False
    
    try:
        # Upload do arquivo
        with open(data_file, 'rb') as file_data:
            object_storage.put_object(
                namespace_name=namespace,
                bucket_name=bucket_name,
                object_name="consolidated_datasource.json",
                put_object_body=file_data,
                content_type="application/json"
            )
        
        print("✅ Upload concluído com sucesso!")
        print(f"   Arquivo: {data_file}")
        print(f"   Bucket: {bucket_name}")
        print(f"   Namespace: {namespace}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
        return False

if __name__ == "__main__":
    upload_to_oci()
