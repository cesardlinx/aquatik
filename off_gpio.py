import sys
import os

working_path = os.getcwd()


def main():
    """Main function"""
    try:
        path = sys.argv[1]
        on_off = sys.argv[2]
    except IndexError:
        print('No ha escrito los argumentos necesarios')
        sys.exit()

    complete_path = os.path.join(working_path, path)

    if os.path.isfile(complete_path):
        with open(complete_path, 'r+') as f:
            list_contents = f.readlines()
            rewrited_contents = []
            if on_off == 'off':
                rewrited_contents = ['# {}'.format(line) if '#' not in line
                                     and ('GPIO' in line
                                     or 'time.sleep' in line)
                                     else line for line in
                                     list_contents]
            elif on_off == 'on':
                rewrited_contents = [line[2:] if line[:2] == '# '
                                     and ('GPIO' in line
                                     or 'time.sleep' in line)
                                     else line[1:] if line[0] == '#'
                                     and ('GPIO' in line
                                     or 'time.sleep' in line)
                                     else line
                                     for line in list_contents]
            else:
                print('Debe escribir si desea agregar los comentarios al GPIO '
                      'o quitarlos')

            string_contents = ''.join(rewrited_contents)
            f.seek(0)
            f.write(string_contents)
    else:
        print('El archivo o la ruta especificada no existe')
        print('Asegurese de haber escrito bien el nombre del archivo')


if __name__ == "__main__":
    main()
