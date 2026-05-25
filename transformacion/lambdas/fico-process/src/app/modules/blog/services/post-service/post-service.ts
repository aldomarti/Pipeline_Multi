import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { environment } from '@environments/environment';
import { GetPostsType } from './post-service.types';

@Injectable()
export class PostService {
  constructor( private http: HttpClient) {
  }

  getPosts(): Observable<GetPostsType> {
    return this.http.get<GetPostsType>(
      `${environment.mockAPI}/posts`
    );
  }
}
