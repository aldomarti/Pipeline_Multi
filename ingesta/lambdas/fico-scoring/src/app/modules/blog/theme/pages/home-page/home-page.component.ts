import { Component, OnInit } from '@angular/core';

import { PostService } from '@blog/services/post-service/post-service';
import { PostType } from '@blog/services/post-service/post-service.types';

@Component({
  selector: 'home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent implements OnInit{
  posts: PostType[]=[];
  constructor(private postService: PostService) {}

  ngOnInit() {
    this.postService.getPosts().subscribe((postResponse)=>{
      this.posts = postResponse.posts
    })
  }
}
