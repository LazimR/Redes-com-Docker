import http from 'k6/http';
import { sleep } from 'k6';
import crypto from 'k6/crypto';

export const options = {
    vus: 80,
    duration: '60s',
};

export default function () {
    const matricula_nome = '20219004610 Lazaro';
    const hash = crypto.sha1(matricula_nome, 'hex');
    const url_nginx = 'http://46.10.0.10/pesado';
    const url_apache = 'http://46.10.0.20/pesado';

    const headers = {
        'X-Custom-ID': hash
    };

    http.get(url_nginx, { headers });
    http.get(url_apache, { headers });

    sleep(1);
}
