import http from 'k6/http';
import crypto from 'k6/crypto';

export const options = {
    stages: [
        { duration: '30s', target: 50 },   // aumento gradual
        { duration: '30s', target: 100 },  // pico
        { duration: '30s', target: 200 },  // carga extrema
        { duration: '30s', target: 0 },    // desaceleração
    ],
};

export default function () {
    const matricula_nome = '20219004610 Lazaro';
    const hash = crypto.sha1(matricula_nome, 'hex');
    const url_nginx = 'http://46.10.0.10/leve';
    const url_apache = 'http://46.10.0.20/leve';

    const headers = {
        'X-Custom-ID': hash
    };

    http.get(url_nginx, { headers });
    http.get(url_apache, { headers });
}
