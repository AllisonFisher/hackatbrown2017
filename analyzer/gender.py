import analyzer

def main():
  data = analyzer.face_detect("img/003.jpg")
  analyzer.create_person("peron_name", "mah_group", data[2][0])


if __name__ == "__main__":
  main()
