import http from 'k6/http';
import { sleep } from 'k6';
import crypto from 'k6/crypto';

export const options = {
    vus: 50,
    duration: '45s',
};

export default function () {
    const matricula_nome = '20219004610 Lazaro';
    const hash = crypto.sha1(matricula_nome, 'hex');
    const url_nginx = 'http://46.10.0.10/medio';
    const url_apache = 'http://46.10.0.20/medio';

    const headers = {
        'X-Custom-ID': hash
    };

    http.get(url_nginx, { headers });
    http.get(url_apache, { headers });

    sleep(1);
}
