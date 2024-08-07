#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>
#include <windows.h>
#include <shobjidl.h>
typedef struct {
    size_t start, end;
} LineRange;
static size_t first_line_cells = 0;
static int is_first_chunk = 1;
void print_hex_position(size_t position) {
    wprintf(L"0x%zx\n", position);
}
void validate_rfc4180_chunk(const char* chunk, size_t chunk_size, size_t start_offset) {
    first_line_cells = 0;
    is_first_chunk = 1;
    size_t* X = malloc((chunk_size) * sizeof(size_t));
    if (!X) {
        wprintf(L"File chunk may be too large.\n");
        return;
    }
    size_t X_count = 0;
    int in_quotes = 0;
    for (size_t i = 0; i < chunk_size - 1; i++) {
        if (chunk[i] == '"') in_quotes = !in_quotes;
        if (chunk[i] == '\r' && chunk[i + 1] == '\n' && !in_quotes) {
            X[X_count++] = i + start_offset;
            if (i > 0 && chunk[i - 1] == ',') {
                wprintf(L"Found comma before CRLF at position ");
                print_hex_position(i - 1 + start_offset);
                free(X);
                return;
            }
        }
    }
    size_t* Y = NULL;
    size_t Y_count = 0;
    for (size_t line = 0; line < X_count; line++) {
        size_t start = (line == 0) ? 0 : X[line - 1] + 2 - start_offset;
        size_t end = X[line] - start_offset;
        if (end > start + 2) {
            Y = malloc((end - start) * sizeof(size_t));
        }
        else {
            wprintf(L"Invalid line. start = %zu, end = %zu\n", start, end);
            free(X);
            return;
        }
        if (!Y) {
            wprintf(L"File may be too large.\n");
            free(X);
            return;
        }
        Y_count = 0;
        in_quotes = 0;
        for (size_t i = start; i < end; i++) {
            if (chunk[i] == '"') in_quotes = !in_quotes;
            if (chunk[i] == ',' && !in_quotes) {
                Y[Y_count++] = i;
            }
        }
        Y[Y_count++] = end;
        if (is_first_chunk) {
            first_line_cells = Y_count;
            is_first_chunk = 0;
        }
        else if (Y_count != first_line_cells && !(line == X_count - 1 && Y_count == 1)) {
            wprintf(L"Inconsistent length of lines at line %zu. Should be %zu, but there be %zu\n", line + 1, first_line_cells, Y_count);
            free(X);
            free(Y);
            return;
        }
        for (size_t cell = 0; cell < Y_count; cell++) {
            size_t cell_start = (cell == 0) ? start : Y[cell - 1] + 1;
            size_t cell_end = Y[cell];
            if (chunk[cell_start] == '"') {
                if (chunk[cell_end - 1] != '"') {
                    wprintf(L"Half-enclosed by double quotes at cell starting ");
                    print_hex_position(cell_start + start_offset);
                    free(X);
                    free(Y);
                    return;
                }
                int quote_count = 0;
                for (size_t i = cell_start; i < cell_end; i++) {
                    if (chunk[i] == '"') quote_count++;
                }
                if (quote_count % 2 != 0) {
                    wprintf(L"Enclosed by double quotes yet has odd number of consistent double quotes at cell starting ");
                    print_hex_position(cell_start + start_offset);
                    free(X);
                    free(Y);
                    return;
                }
            }
            else {
                for (size_t i = cell_start; i < cell_end; i++) {
                    if (chunk[i] == '"') {
                        wprintf(L"Not enclosed by double quotes yet includes double quotes at cell starting ");
                        print_hex_position(cell_start + start_offset);
                        free(X);
                        free(Y);
                        return;
                    }
                }
            }
        }
        free(Y);
    }
    wprintf(L"RFC 4180 compliant\n");
    free(X);
}
void validate_rfc4180(const char* filename) {
    FILE* file = NULL;
    errno_t err = fopen_s(&file, filename, "rb");
    if (err != 0 || !file) {
        printf("Error reading file: %s\n", filename);
        return;
    }
    const size_t min_chunk_size = (size_t)(128LL * 1024 * 1024);
    size_t offset = 0;
    size_t read_size = 0;
    char* buffer = NULL;
    size_t buffer_size = 0;
    while (1) {
        buffer_size = 2 * min_chunk_size + 2;
        buffer = malloc(buffer_size);
        if (!buffer) {
            wprintf(L"Failed to malloc buffer of size: ");
            print_hex_position(buffer_size);
            fclose(file);
            return;
        }
        read_size = fread(buffer, 1, buffer_size - 1, file);
        if (read_size == 0) {
            free(buffer);
            break;
        }
        buffer[read_size] = '\0';
        size_t count_quotes = 0;
        size_t last_crlf_pos = 0;
        for (size_t i = 0; i < read_size; i++) {
            if (buffer[i] == 0x22) count_quotes++;
            if (i > min_chunk_size + 1 && buffer[i] == '\n' && buffer[i - 1] == '\r') {
                if (count_quotes % 2 == 0) {
                    last_crlf_pos = i + 1;
                    break;
                }
            }
        }
        while (count_quotes % 2 != 0) {
            char c;
            if (fread(&c, 1, 1, file) == 0) break;
            buffer[read_size] = c;
            read_size++;
            buffer[read_size] = '\0';
            if (c == 0x22) count_quotes++;
            if (c == '\n' && buffer[read_size - 2] == '\r') {
                if (count_quotes % 2 == 0) {
                    last_crlf_pos = read_size;
                    break;
                }
            }
        }
        if (last_crlf_pos == 0) {
            last_crlf_pos = read_size;
        }
        char* chunk = malloc(last_crlf_pos + 1);
        if (!chunk) {
            wprintf(L"Failed to malloc chunk of size: ");
            print_hex_position(last_crlf_pos);
            free(buffer);
            fclose(file);
            return;
        }
        memcpy(chunk, buffer, last_crlf_pos);
        chunk[last_crlf_pos] = '\0';
        fseek(file, (long)(last_crlf_pos - read_size), SEEK_CUR);
        read_size = last_crlf_pos;
        if (offset > 0) {
            wprintf(L"offset = ");
            print_hex_position(offset);
        }
        validate_rfc4180_chunk(chunk, read_size, offset);
        offset += read_size;
        free(chunk);
        free(buffer);
        if (feof(file)) {
            break;
        }
    }
    fclose(file);
}
void process_directory(const wchar_t* directory_path) {
    wchar_t search_path[MAX_PATH];
    HANDLE hFind;
    WIN32_FIND_DATAW findFileData;
    swprintf_s(search_path, MAX_PATH, L"%s\\*.csv", directory_path);
    hFind = FindFirstFileW(search_path, &findFileData);
    if (hFind == INVALID_HANDLE_VALUE) {
        wprintf(L"Failed to find CSV files in the directory: %s\n", directory_path);
        return;
    }
    do {
        if (!(findFileData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
            wchar_t file_path[MAX_PATH];
            swprintf_s(file_path, MAX_PATH, L"%ls\\%ls", directory_path, findFileData.cFileName);
            wprintf(L"Processing file: %s\n", file_path);
            char file_path_mb[MAX_PATH];
            size_t converted_chars;
            if (wcstombs_s(&converted_chars, file_path_mb, MAX_PATH, file_path, _TRUNCATE) != 0) {
                wprintf(L"Failed to convert file path to multibyte: %s\n", file_path);
                continue;
            }
            first_line_cells = 0;
            is_first_chunk = 1;
            validate_rfc4180(file_path_mb);
        }
    } while (FindNextFileW(hFind, &findFileData) != 0);
    FindClose(hFind);
}
int select_file_via_dialog(wchar_t* selected_path, size_t max_path_length) {
    HRESULT hr;
    IFileOpenDialog* pFileOpen = NULL;
    IShellItem* pItem = NULL;
    PWSTR pszFilePath = NULL;
    hr = CoInitializeEx(NULL, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE);
    if (FAILED(hr)) {
        wprintf(L"Failed to initialize COM library.\n");
        return 0;
    }
    hr = CoCreateInstance(&CLSID_FileOpenDialog, NULL, CLSCTX_ALL, &IID_IFileOpenDialog, (void**)&pFileOpen);
    if (FAILED(hr)) {
        wprintf(L"Failed to create FileOpenDialog instance.\n");
        goto cleanup;
    }
    COMDLG_FILTERSPEC rgSpec[] = { {L"CSV Files", L"*.csv"} };
    hr = pFileOpen->lpVtbl->SetFileTypes(pFileOpen, ARRAYSIZE(rgSpec), rgSpec);
    if (FAILED(hr)) {
        wprintf(L"Failed to set file types.\n");
        goto cleanup;
    }
    hr = pFileOpen->lpVtbl->Show(pFileOpen, NULL);
    if (FAILED(hr)) {
        wprintf(L"No file selected or an error occurred.\n");
        goto cleanup;
    }
    hr = pFileOpen->lpVtbl->GetResult(pFileOpen, &pItem);
    if (FAILED(hr)) {
        wprintf(L"Failed to get dialog result.\n");
        goto cleanup;
    }
    hr = pItem->lpVtbl->GetDisplayName(pItem, SIGDN_FILESYSPATH, &pszFilePath);
    if (FAILED(hr)) {
        wprintf(L"Failed to get file path.\n");
        goto cleanup;
    }
    wcsncpy_s(selected_path, max_path_length, pszFilePath, _TRUNCATE);
    selected_path[max_path_length - 1] = L'\0';
cleanup:
    if (pszFilePath) CoTaskMemFree(pszFilePath);
    if (pItem) pItem->lpVtbl->Release(pItem);
    if (pFileOpen) pFileOpen->lpVtbl->Release(pFileOpen);
    CoUninitialize();
    return SUCCEEDED(hr) ? 1 : 0;
}
int wmain(int argc, wchar_t* argv[]) {
    wchar_t path[MAX_PATH];
    if (argc == 2) {
        wcsncpy_s(path, MAX_PATH, argv[1], _TRUNCATE);
        path[MAX_PATH - 1] = L'\0';
    }
    else if (argc == 1) {
        if (!select_file_via_dialog(path, MAX_PATH)) {
            wprintf(L"Failed to select a file.\n");
            return 1;
        }
    }
    else {
        wprintf(L"Too much arguments.\n");
        return 1;
    }
    WIN32_FILE_ATTRIBUTE_DATA fileInfo = { 0 };
    if (GetFileAttributesExW(path, GetFileExInfoStandard, &fileInfo)) {
        if (fileInfo.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
            process_directory(path);
        }
        else {
            char path_mb[MAX_PATH];
            size_t converted_chars;
            if (wcstombs_s(&converted_chars, path_mb, MAX_PATH, path, _TRUNCATE) != 0) {
                wprintf(L"Failed to convert file path to multibyte: %s\n", path);
                return 1;
            }
            validate_rfc4180(path_mb);
            wprintf(L"Finished. Press any key to terminate the program.\n");
            return getchar();
        }
    }
    else {
        wprintf(L"Failed to get file attributes for: %s\n", path);
        return 1;
    }
    return 0;
}