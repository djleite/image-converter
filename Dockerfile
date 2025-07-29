FROM continuumio/miniconda3

# Copy environment definition
COPY environment.yml .

# Create conda environment
RUN conda env create -f environment.yml

# Use that environment
SHELL ["conda", "run", "-n", "image-env", "/bin/bash", "-c"]

WORKDIR /app
COPY convert_and_rename.py .
RUN chmod +x convert_and_rename.py

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "image-env", "python", "convert_and_rename.py"]
