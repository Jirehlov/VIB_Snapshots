#include <Windows.h>
#include <winhttp.h>
#pragma comment(lib, "winhttp.lib")
void __chkstk() {
}
int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    HINTERNET hSession, hConnect, hRequest;
    HANDLE hFile;
    DWORD dwSize = 0, dwDownloaded = 0;
    BYTE buffer[4096];
    hSession = WinHttpOpen(L"WINAPI", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
    if (!hSession) ExitProcess(1);
    DWORD dwHttp2 = WINHTTP_PROTOCOL_FLAG_HTTP2;
    if (!WinHttpSetOption(hSession, WINHTTP_OPTION_ENABLE_HTTP_PROTOCOL, &dwHttp2, sizeof(dwHttp2))) {
        ExitProcess(1);
    }
    hConnect = WinHttpConnect(hSession, L"jirehlov.com", INTERNET_DEFAULT_HTTPS_PORT, 0);
    if (!hConnect) goto cleanup;
    hRequest = WinHttpOpenRequest(hConnect, L"GET", L"/sorted.csv", NULL, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, WINHTTP_FLAG_SECURE);
    if (!hRequest) goto cleanup;
    if (!WinHttpSendRequest(hRequest, WINHTTP_NO_ADDITIONAL_HEADERS, 0, WINHTTP_NO_REQUEST_DATA, 0, 0, 0) ||
        !WinHttpReceiveResponse(hRequest, NULL)) goto cleanup;
    hFile = CreateFileW(L"sorted1.csv", GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) goto cleanup;
    while (WinHttpQueryDataAvailable(hRequest, &dwSize) && dwSize > 0) {
        if (dwSize > sizeof(buffer)) dwSize = sizeof(buffer);
        if (WinHttpReadData(hRequest, buffer, dwSize, &dwDownloaded) && dwDownloaded > 0) {
            WriteFile(hFile, buffer, dwDownloaded, NULL, NULL);
        }
    }
    CloseHandle(hFile);
cleanup:
    if (hRequest) WinHttpCloseHandle(hRequest);
    if (hConnect) WinHttpCloseHandle(hConnect);
    if (hSession) WinHttpCloseHandle(hSession);
    ExitProcess(0);
}
