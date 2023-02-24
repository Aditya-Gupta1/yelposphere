variable "datalake_name" {
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
}

variable "region" {
  description = "Region for GCP resources."
  type = string
}